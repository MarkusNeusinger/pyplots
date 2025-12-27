"""
Tests for api/cache.py caching utilities.
"""


from api.cache import cache_key, get_cached, set_cached


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
    """Tests for get_cached and set_cached functions."""

    def test_get_nonexistent_returns_none(self) -> None:
        """Getting nonexistent key should return None."""
        result = get_cached("nonexistent_key_12345")
        assert result is None

    def test_set_and_get(self) -> None:
        """Setting and getting a value should work."""
        test_key = "test_key_set_get"
        test_value = {"data": "test_value"}

        set_cached(test_key, test_value)
        result = get_cached(test_key)

        assert result == test_value

    def test_overwrite_value(self) -> None:
        """Setting same key twice should overwrite."""
        test_key = "test_key_overwrite"

        set_cached(test_key, "first")
        set_cached(test_key, "second")

        assert get_cached(test_key) == "second"

    def test_cache_complex_types(self) -> None:
        """Cache should handle complex types."""
        test_key = "test_key_complex"
        test_value = {
            "list": [1, 2, 3],
            "nested": {"a": 1, "b": 2},
            "tuple": (1, 2, 3),
        }

        set_cached(test_key, test_value)
        result = get_cached(test_key)

        assert result == test_value
