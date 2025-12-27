"""
Caching utilities for pyplots API.

Centralized cache management with consistent key patterns.
"""

from typing import Any

from cachetools import TTLCache


# Global cache instance (1000 entries, 10 min TTL)
_cache: TTLCache = TTLCache(maxsize=1000, ttl=600)


def cache_key(*parts: str) -> str:
    """
    Build consistent cache key from parts.

    Args:
        *parts: Key components to join.

    Returns:
        Cache key string.

    Example:
        >>> cache_key("spec", "scatter-basic")
        "spec:scatter-basic"
    """
    return ":".join(str(p) for p in parts if p)


def get_cached(key: str) -> Any | None:
    """
    Get value from cache.

    Args:
        key: Cache key.

    Returns:
        Cached value or None if not found.
    """
    return _cache.get(key)


def set_cached(key: str, value: Any) -> None:
    """
    Set value in cache.

    Args:
        key: Cache key.
        value: Value to cache.
    """
    _cache[key] = value
