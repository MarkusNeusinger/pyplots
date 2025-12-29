"""
Caching utilities for pyplots API.

Centralized cache management with consistent key patterns.
"""

from typing import Any

from cachetools import TTLCache

from core.config import settings


# Global cache instance (configured via settings)
_cache: TTLCache = TTLCache(maxsize=settings.cache_maxsize, ttl=settings.cache_ttl)


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


def get_cache(key: str) -> Any | None:
    """
    Get value from cache.

    Args:
        key: Cache key.

    Returns:
        Cached value or None if not found.
    """
    return _cache.get(key)


def set_cache(key: str, value: Any) -> None:
    """
    Set value in cache.

    Args:
        key: Cache key.
        value: Value to cache.
    """
    _cache[key] = value


def clear_cache() -> None:
    """
    Clear entire cache.

    Use this when you want to invalidate all cached data.
    Called automatically after database synchronization.

    Example:
        >>> clear_cache()  # Invalidates all cached responses
    """
    _cache.clear()


def clear_cache_by_pattern(pattern: str) -> int:
    """
    Clear cache entries matching a pattern.

    Args:
        pattern: String pattern to match (substring match)

    Returns:
        Number of cache entries cleared

    Example:
        >>> clear_cache_by_pattern("spec:")  # Clears all spec-related cache
        15
        >>> clear_cache_by_pattern("filter:")  # Clears all filter cache
        42
    """
    keys_to_delete = [key for key in _cache.keys() if pattern in key]
    for key in keys_to_delete:
        del _cache[key]
    return len(keys_to_delete)


def clear_spec_cache(spec_id: str) -> int:
    """
    Clear all cache entries related to a specific spec.

    Clears spec detail, spec images, spec list, filters, and stats caches.

    Args:
        spec_id: The specification ID

    Returns:
        Total count across all cleared patterns (may count overlapping keys multiple times)

    Example:
        >>> clear_spec_cache("scatter-basic")
        5
    """
    # Clear spec detail, spec images, and spec list cache
    count = 0
    count += clear_cache_by_pattern(f"spec:{spec_id}")
    count += clear_cache_by_pattern(f"spec_images:{spec_id}")
    count += clear_cache_by_pattern("specs_list")  # List might have changed
    count += clear_cache_by_pattern("filter:")  # Filters might be affected
    count += clear_cache_by_pattern("stats")  # Stats might have changed
    return count


def clear_library_cache(library_id: str) -> int:
    """
    Clear all cache entries for a specific library.

    Args:
        library_id: The library ID

    Returns:
        Number of cache entries cleared

    Example:
        >>> clear_library_cache("matplotlib")
        3
    """
    # Clear library images and lists
    count = 0
    count += clear_cache_by_pattern(f"lib_images:{library_id}")
    count += clear_cache_by_pattern("libraries")  # List might have changed
    count += clear_cache_by_pattern("filter:")  # Filters might be affected
    count += clear_cache_by_pattern("stats")  # Stats might have changed
    return count


def get_cache_stats() -> dict:
    """
    Get cache statistics.

    Returns:
        Dict with cache size, maxsize, and TTL

    Example:
        >>> get_cache_stats()
        {"size": 42, "maxsize": 1000, "ttl": 600}
    """
    return {"size": len(_cache), "maxsize": _cache.maxsize, "ttl": _cache.ttl}
