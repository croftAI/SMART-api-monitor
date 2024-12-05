# api/middleware/rate_limiter.py

from fastapi import Request, HTTPException
import time
from typing import Dict, Tuple
from collections import defaultdict
import asyncio


class RateLimiter:
    """Rate limiting middleware with sliding window."""

    def __init__(
            self,
            rate_limit: int = 100,  # requests per window
            window_size: int = 60  # window size in seconds
    ):
        self.rate_limit = rate_limit
        self.window_size = window_size
        self.windows: Dict[str, Dict[float, int]] = defaultdict(dict)
        self.locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def __call__(
            self,
            request: Request,
            call_next
    ):
        # Get client identifier (IP or API key)
        client_id = self._get_client_id(request)

        # Check rate limit
        async with self.locks[client_id]:
            if await self._is_rate_limited(client_id):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )

            # Update request count
            self._update_window(client_id)

        return await call_next(request)

    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier."""
        # Prefer API key if available
        api_key = request.headers.get('X-API-Key')
        if api_key:
            return f"apikey_{api_key}"

        # Fallback to IP address
        return f"ip_{request.client.host}"

    async def _is_rate_limited(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit."""
        current_time = time.time()
        window = self.windows[client_id]

        # Remove old timestamps
        cutoff = current_time - self.window_size
        window = {ts: count for ts, count in window.items() if ts > cutoff}
        self.windows[client_id] = window

        # Count total requests in window
        total_requests = sum(window.values())

        return total_requests >= self.rate_limit

    def _update_window(self, client_id: str):
        """Update request count for current timestamp."""
        current_time = time.time()
        if current_time in self.windows[client_id]:
            self.windows[client_id][current_time] += 1
        else:
            self.windows[client_id][current_time] = 1