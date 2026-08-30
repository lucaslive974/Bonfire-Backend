import threading
import time
from typing import Any, Dict, Optional, Tuple

from .interface import ICache


class InMemoryCache(ICache):
    """
    Thread-safe in-memory cache implementation.
    Drop-in ready to be replaced by RedisCache in the future.
    """
    def __init__(self):
        # Store dict: key -> (value, expiry_timestamp_or_None)
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._store:
                return None
            
            value, expiry = self._store[key]
            if expiry is not None and time.time() > expiry:
                # Lazy expiration
                del self._store[key]
                return None
            
            return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        expiry = time.time() + ttl_seconds if ttl_seconds is not None else None
        with self._lock:
            self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
