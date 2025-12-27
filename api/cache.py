"""
Caching utilities for pyplots API.

Centralized cache management with consistent key patterns.
"""

from functools import wraps
from typing import Any, Callable, TypeVar

from cachetools import TTLCache


# Global cache instance (1000 entries, 10 min TTL)
_cache: TTLCache = TTLCache(maxsize=1000, ttl=600)

T = TypeVar("T")


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


def delete_cached(key: str) -> None:
    """
    Delete value from cache.

    Args:
        key: Cache key to delete.
    """
    _cache.pop(key, None)


def clear_cache() -> None:
    """Clear all cached values."""
    _cache.clear()


def clear_pattern(pattern: str) -> int:
    """
    Clear all keys matching pattern prefix.

    Args:
        pattern: Key prefix to match.

    Returns:
        Number of keys deleted.
    """
    keys_to_delete = [k for k in _cache if k.startswith(pattern)]
    for key in keys_to_delete:
        del _cache[key]
    return len(keys_to_delete)


def cached(key_prefix: str):
    """
    Decorator for caching function results.

    Args:
        key_prefix: Prefix for cache key.

    Example:
        @cached("specs")
        async def get_all_specs():
            ...
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Build cache key from prefix and args
            key = cache_key(key_prefix, *[str(a) for a in args], *[f"{k}={v}" for k, v in sorted(kwargs.items())])

            # Check cache
            if key in _cache:
                return _cache[key]

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            _cache[key] = result
            return result

        return wrapper

    return decorator


def cache_stats() -> dict:
    """
    Get cache statistics.

    Returns:
        Dict with cache size and max size.
    """
    return {
        "size": len(_cache),
        "maxsize": _cache.maxsize,
        "ttl": _cache.ttl,
    }
