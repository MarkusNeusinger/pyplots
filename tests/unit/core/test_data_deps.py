"""
Smoke tests for numpy and pandas API compatibility.

These tests exercise the exact API patterns used in the project (conftest.py fixtures,
plot implementations) to catch breaking changes in major version upgrades.

numpy 2.x removed many deprecated functions.
pandas 3.x made Copy-on-Write the default.
"""

import numpy as np
import pandas as pd


class TestNumpyApiCompatibility:
    """Tests for numpy API patterns used in the project."""

    def test_random_seed(self) -> None:
        """np.random.seed() must be available (used in conftest and plots)."""
        np.random.seed(42)
        val1 = np.random.randn(5)
        np.random.seed(42)
        val2 = np.random.randn(5)
        np.testing.assert_array_equal(val1, val2)

    def test_random_randn(self) -> None:
        """np.random.randn() must return correct shape (used in conftest)."""
        result = np.random.randn(50)
        assert result.shape == (50,)
        assert result.dtype == np.float64

    def test_random_uniform(self) -> None:
        """np.random.uniform() must work with low/high/size (used in conftest)."""
        result = np.random.uniform(10, 100, 50)
        assert result.shape == (50,)
        assert result.min() >= 10
        assert result.max() <= 100

    def test_random_choice(self) -> None:
        """np.random.choice() must work with list and size (used in conftest)."""
        result = np.random.choice(["A", "B", "C"], 50)
        assert result.shape == (50,)
        assert set(result).issubset({"A", "B", "C"})

    def test_linspace(self) -> None:
        """np.linspace() must work (commonly used in plot implementations)."""
        result = np.linspace(0, 10, 100)
        assert result.shape == (100,)
        assert result[0] == 0.0
        assert result[-1] == 10.0

    def test_array_creation(self) -> None:
        """np.array() must work for basic list conversion (used in plots)."""
        result = np.array([1, 2, 3])
        assert result.shape == (3,)
        assert result.dtype in (np.int64, np.intp)

    def test_arange(self) -> None:
        """np.arange() must work (commonly used in plot implementations)."""
        result = np.arange(0, 10, 0.5)
        assert len(result) == 20
        assert result[0] == 0.0


class TestPandasApiCompatibility:
    """Tests for pandas API patterns used in the project."""

    def test_dataframe_from_dict(self) -> None:
        """pd.DataFrame() from dict must work (used in conftest)."""
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "x": np.random.randn(50),
                "y": np.random.randn(50),
                "category": np.random.choice(["A", "B", "C"], 50),
                "size": np.random.uniform(10, 100, 50),
            }
        )
        assert df.shape == (50, 4)
        assert list(df.columns) == ["x", "y", "category", "size"]

    def test_column_access(self) -> None:
        """Column access via df['col'] and df.col must work."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        assert list(df["a"]) == [1, 2, 3]
        assert list(df.b) == [4, 5, 6]

    def test_to_dict(self) -> None:
        """df.to_dict() must work (used in API responses)."""
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = df.to_dict()
        assert result == {"a": {0: 1, 1: 2}, "b": {0: 3, 1: 4}}

    def test_dtypes(self) -> None:
        """DataFrame dtypes must be accessible."""
        df = pd.DataFrame({"x": [1.0, 2.0], "cat": ["A", "B"]})
        assert df["x"].dtype == np.float64
        # pandas 3.x uses StringDtype by default, pandas 2.x uses object
        assert pd.api.types.is_string_dtype(df["cat"])

    def test_copy_on_write_safe_pattern(self) -> None:
        """Modifying a copy should not affect the original (pandas 3.x CoW)."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        df_copy = df.copy()
        df_copy["a"] = [10, 20, 30]
        # Original must be unchanged
        assert list(df["a"]) == [1, 2, 3]
