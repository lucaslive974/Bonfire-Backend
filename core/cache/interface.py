from abc import ABC, abstractmethod
from typing import Any, Optional


class ICache(ABC):
    """Generic interface for application-wide caching."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from the cache by its key. Returns None if not found or expired."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Store a value in the cache with an optional time-to-live in seconds."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove a value from the cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all values from the cache."""
        pass
