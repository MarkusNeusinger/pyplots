"""
Tests for api/cache.py caching utilities.
"""

from api.cache import (
    cache_key,
    clear_cache,
    clear_cache_by_pattern,
    clear_library_cache,
    clear_spec_cache,
    get_cache,
    get_cache_stats,
    set_cache,
)


class TestCacheKey:
    """Tests for cache_key function."""

    def test_single_part(self) -> None:
        """Single part should return as-is."""
        assert cache_key("specs") == "specs"

    def test_multiple_parts(self) -> None:
        """Multiple parts should be joined with colon."""
        assert cache_key("spec", "scatter-basic") == "spec:scatter-basic"

    def test_three_parts(self) -> None:
        """Three parts should be joined with colons."""
        assert cache_key("lib", "images", "matplotlib") == "lib:images:matplotlib"

    def test_empty_parts_filtered(self) -> None:
        """Empty strings should be filtered out."""
        assert cache_key("spec", "", "scatter") == "spec:scatter"

    def test_none_parts_filtered(self) -> None:
        """None values should be filtered out."""
        assert cache_key("spec", None, "scatter") == "spec:scatter"  # type: ignore

    def test_empty_input(self) -> None:
        """Empty input should return empty string."""
        assert cache_key() == ""


class TestCacheOperations:
    """Tests for get_cache and set_cache functions."""

    def test_get_nonexistent_returns_none(self) -> None:
        """Getting nonexistent key should return None."""
        result = get_cache("nonexistent_key_12345")
        assert result is None

    def test_set_and_get(self) -> None:
        """Setting and getting a value should work."""
        test_key = "test_key_set_get"
        test_value = {"data": "test_value"}

        set_cache(test_key, test_value)
        result = get_cache(test_key)

        assert result == test_value

    def test_overwrite_value(self) -> None:
        """Setting same key twice should overwrite."""
        test_key = "test_key_overwrite"

        set_cache(test_key, "first")
        set_cache(test_key, "second")

        assert get_cache(test_key) == "second"

    def test_cache_complex_types(self) -> None:
        """Cache should handle complex types."""
        test_key = "test_key_complex"
        test_value = {"list": [1, 2, 3], "nested": {"a": 1, "b": 2}, "tuple": (1, 2, 3)}

        set_cache(test_key, test_value)
        result = get_cache(test_key)

        assert result == test_value


class TestClearCache:
    """Tests for clear_cache function."""

    def test_clear_all_cache(self) -> None:
        """Should clear all cache entries."""
        # Set multiple cache entries
        set_cache("key1", "value1")
        set_cache("key2", "value2")
        set_cache("key3", "value3")

        # Clear cache
        clear_cache()

        # All should be gone
        assert get_cache("key1") is None
        assert get_cache("key2") is None
        assert get_cache("key3") is None

    def test_clear_empty_cache(self) -> None:
        """Should work with empty cache."""
        clear_cache()  # Should not raise
        assert get_cache_stats()["size"] == 0


class TestClearCacheByPattern:
    """Tests for clear_cache_by_pattern function."""

    def test_clear_matching_pattern(self) -> None:
        """Should clear only entries matching pattern."""
        # Set cache entries
        set_cache("spec:scatter-basic", "value1")
        set_cache("spec:bar-chart", "value2")
        set_cache("filter:matplotlib", "value3")

        # Clear spec entries
        count = clear_cache_by_pattern("spec:")

        # Should have cleared 2 entries
        assert count == 2
        assert get_cache("spec:scatter-basic") is None
        assert get_cache("spec:bar-chart") is None
        assert get_cache("filter:matplotlib") is not None  # Not cleared

    def test_clear_no_matches(self) -> None:
        """Should return 0 when no entries match."""
        set_cache("key1", "value1")
        count = clear_cache_by_pattern("nonexistent")
        assert count == 0
        assert get_cache("key1") is not None  # Still there

    def test_clear_substring_match(self) -> None:
        """Should match pattern as substring."""
        set_cache("prefix:middle:suffix", "value")
        count = clear_cache_by_pattern("middle")
        assert count == 1
        assert get_cache("prefix:middle:suffix") is None


class TestClearSpecCache:
    """Tests for clear_spec_cache function."""

    def test_clear_spec_entries(self) -> None:
        """Should clear all spec-related cache entries."""
        # Set various cache entries
        set_cache("spec:scatter-basic", "spec detail")
        set_cache("spec_images:scatter-basic", "spec images")
        set_cache("specs_list", "all specs")
        set_cache("filter:lib=matplotlib", "filter result")
        set_cache("stats", "stats data")
        set_cache("unrelated:key", "unrelated")

        # Clear spec cache
        count = clear_spec_cache("scatter-basic")

        # Should have cleared spec-related entries
        assert count > 0
        assert get_cache("spec:scatter-basic") is None
        assert get_cache("spec_images:scatter-basic") is None
        assert get_cache("specs_list") is None
        assert get_cache("filter:lib=matplotlib") is None
        assert get_cache("stats") is None

        # Unrelated should still be there
        assert get_cache("unrelated:key") is not None

    def test_clear_spec_returns_count(self) -> None:
        """Should return number of cleared entries."""
        set_cache("spec:scatter-basic", "value")
        set_cache("spec_images:scatter-basic", "value")

        count = clear_spec_cache("scatter-basic")
        assert isinstance(count, int)
        assert count >= 2  # At least the 2 we set


class TestClearLibraryCache:
    """Tests for clear_library_cache function."""

    def test_clear_library_entries(self) -> None:
        """Should clear all library-related cache entries."""
        # Set various cache entries
        set_cache("lib_images:matplotlib", "lib images")
        set_cache("libraries", "all libraries")
        set_cache("filter:lib=matplotlib", "filter result")
        set_cache("stats", "stats data")
        set_cache("unrelated:key", "unrelated")

        # Clear library cache
        count = clear_library_cache("matplotlib")

        # Should have cleared library-related entries
        assert count > 0
        assert get_cache("lib_images:matplotlib") is None
        assert get_cache("libraries") is None
        assert get_cache("filter:lib=matplotlib") is None
        assert get_cache("stats") is None

        # Unrelated should still be there
        assert get_cache("unrelated:key") is not None

    def test_clear_library_returns_count(self) -> None:
        """Should return number of cleared entries."""
        set_cache("lib_images:matplotlib", "value")
        set_cache("libraries", "value")

        count = clear_library_cache("matplotlib")
        assert isinstance(count, int)
        assert count >= 2


class TestGetCacheStats:
    """Tests for get_cache_stats function."""

    def test_stats_structure(self) -> None:
        """Should return dict with size, maxsize, and ttl."""
        stats = get_cache_stats()

        assert isinstance(stats, dict)
        assert "size" in stats
        assert "maxsize" in stats
        assert "ttl" in stats

    def test_stats_size_accuracy(self) -> None:
        """Size should reflect number of cache entries."""
        # Clear cache first
        clear_cache()

        # Add entries
        set_cache("key1", "value1")
        set_cache("key2", "value2")

        stats = get_cache_stats()
        assert stats["size"] == 2

    def test_stats_types(self) -> None:
        """Stats values should be correct types."""
        stats = get_cache_stats()

        assert isinstance(stats["size"], int)
        assert isinstance(stats["maxsize"], int)
        assert isinstance(stats["ttl"], (int, float))
