# api/middleware/logging_middleware.py

from fastapi import Request, Response
from typing import Callable
import logging
import time
import uuid
from datetime import datetime


class LoggingMiddleware:
    """Request/response logging middleware."""

    def __init__(self):
        self.logger = logging.getLogger("smart_api")
        self._setup_logger()

    def _setup_logger(self):
        """Configure logger settings."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def __call__(
            self,
            request: Request,
            call_next: Callable
    ) -> Response:
        # Generate trace ID
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        # Log request
        await self._log_request(request, trace_id)

        # Process request and measure timing
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # Log response
        self._log_response(request, response, duration, trace_id)

        return response

    async def _log_request(self, request: Request, trace_id: str):
        """Log incoming request details."""
        body = await self._get_request_body(request)
        self.logger.info({
            'event': 'request',
            'timestamp': datetime.now().isoformat(),
            'trace_id': trace_id,
            'method': request.method,
            'path': request.url.path,
            'query_params': str(request.query_params),
            'body': body,
            'headers': dict(request.headers)
        })

    def _log_response(
            self,
            request: Request,
            response: Response,
            duration: float,
            trace_id: str
    ):
        """Log response details."""
        self.logger.info({
            'event': 'response',
            'timestamp': datetime.now().isoformat(),
            'trace_id': trace_id,
            'method': request.method,
            'path': request.url.path,
            'status_code': response.status_code,
            'duration': f"{duration:.3f}s",
            'headers': dict(response.headers)
        })

    async def _get_request_body(self, request: Request) -> str:
        """Safely get request body content."""
        try:
            body = await request.body()
            return body.decode()
        except Exception:
            return ""