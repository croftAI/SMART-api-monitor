from typing import Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict


class CacheManager:
    def __init__(self, max_size: int = 1000,
                 ttl: timedelta = timedelta(minutes=5)):
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, datetime] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self.cache:
            return None

        if self._is_expired(key):
            self.delete(key)
            return None

        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: Any):
        """Set value in cache with TTL."""
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        self.cache[key] = value
        self.timestamps[key] = datetime.now()
        self.cache.move_to_end(key)

    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired."""
        if key not in self.timestamps:
            return True
        return datetime.now() - self.timestamps[key] > self.ttl