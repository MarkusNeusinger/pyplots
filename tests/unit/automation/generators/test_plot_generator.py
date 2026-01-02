"""Tests for automation.generators.plot_generator module."""

from unittest.mock import MagicMock, patch

import pytest

from automation.generators.plot_generator import extract_and_validate_code, retry_with_backoff


class TestExtractAndValidateCode:
    """Tests for extract_and_validate_code function."""

    def test_extract_plain_code(self):
        response = """import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.savefig('plot.png')"""

        result = extract_and_validate_code(response)

        assert "import matplotlib" in result
        assert "plt.plot" in result
        assert "plt.savefig" in result

    def test_extract_from_markdown_python(self):
        response = """Here is the implementation:

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.randn(100)
plt.scatter(x, x * 0.5)
plt.savefig('plot.png')
```

This creates a simple scatter plot."""

        result = extract_and_validate_code(response)

        assert "import matplotlib" in result
        assert "import numpy" in result
        assert "np.random.seed(42)" in result
        assert "Here is the implementation" not in result
        assert "This creates" not in result

    def test_extract_from_generic_markdown(self):
        response = """```
import numpy as np
x = np.array([1, 2, 3])
print(x)
```"""

        result = extract_and_validate_code(response)

        assert "import numpy" in result
        assert "np.array" in result

    def test_extract_code_with_multiple_blocks(self):
        """Should extract from first python block."""
        response = """Here's an example:

```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
```

And here's another:

```python
print("second block")
```
"""

        result = extract_and_validate_code(response)

        assert "import matplotlib" in result
        assert "plt.plot" in result
        # Should only get first block
        assert "second block" not in result

    def test_empty_code_raises_value_error(self):
        with pytest.raises(ValueError, match="No code could be extracted"):
            extract_and_validate_code("")

    def test_whitespace_only_raises_value_error(self):
        with pytest.raises(ValueError, match="No code could be extracted"):
            extract_and_validate_code("   \n\n   ")

    def test_empty_code_block_raises_value_error(self):
        response = """```python
```"""

        with pytest.raises(ValueError, match="No code could be extracted"):
            extract_and_validate_code(response)

    def test_syntax_error_raises_value_error(self):
        response = """```python
def broken(
    print("missing closing paren"
```"""

        with pytest.raises(ValueError, match="syntax errors"):
            extract_and_validate_code(response)

    def test_indentation_error_raises(self):
        response = """```python
def foo():
print("bad indent")
```"""

        with pytest.raises(ValueError, match="syntax errors"):
            extract_and_validate_code(response)

    def test_valid_complex_code(self):
        response = """```python
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

def create_plot(title: Optional[str] = None) -> None:
    np.random.seed(42)
    x = np.random.randn(100)
    y = x * 0.8 + np.random.randn(100) * 0.5

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(x, y, alpha=0.7)

    if title:
        ax.set_title(title)

    plt.savefig('plot.png', dpi=300)

if __name__ == '__main__':
    create_plot('Scatter Plot')
```"""

        result = extract_and_validate_code(response)

        assert "np.random.seed(42)" in result
        assert "figsize=(16, 9)" in result
        assert "def create_plot" in result
        assert "Optional[str]" in result

    def test_code_with_comments_and_docstrings(self):
        response = '''```python
"""Module docstring."""

import matplotlib.pyplot as plt

# Create a simple plot
def plot_data():
    """Create and save a plot."""
    plt.plot([1, 2, 3])  # inline comment
    plt.savefig("output.png")
```'''

        result = extract_and_validate_code(response)

        assert '"""Module docstring."""' in result
        assert "# Create a simple plot" in result
        assert "# inline comment" in result

    def test_code_with_f_strings(self):
        response = """```python
name = "test"
value = 42
print(f"Name: {name}, Value: {value}")
```"""

        result = extract_and_validate_code(response)

        assert 'f"Name: {name}' in result

    def test_preserves_newlines_in_code(self):
        response = """```python
import matplotlib.pyplot as plt


def func1():
    pass


def func2():
    pass
```"""

        result = extract_and_validate_code(response)

        # Should preserve blank lines
        assert "\n\n" in result


class TestRetryWithBackoff:
    """Tests for retry_with_backoff function."""

    def test_success_on_first_try(self):
        func = MagicMock(return_value="success")

        result = retry_with_backoff(func, max_retries=3)

        assert result == "success"
        assert func.call_count == 1

    def test_retry_on_rate_limit_error(self):
        from anthropic import RateLimitError

        mock_response = MagicMock()
        mock_response.status_code = 429

        func = MagicMock(
            side_effect=[RateLimitError(message="rate limited", response=mock_response, body={}), "success"]
        )

        with patch("time.sleep"):  # Skip actual sleep
            result = retry_with_backoff(func, max_retries=3, initial_delay=0.01)

        assert result == "success"
        assert func.call_count == 2

    def test_retry_on_connection_error(self):
        from anthropic import APIConnectionError

        mock_request = MagicMock()

        func = MagicMock(
            side_effect=[
                APIConnectionError(message="connection failed", request=mock_request),
                APIConnectionError(message="connection failed again", request=mock_request),
                "success",
            ]
        )

        with patch("time.sleep"):
            result = retry_with_backoff(func, max_retries=3, initial_delay=0.01)

        assert result == "success"
        assert func.call_count == 3

    def test_max_retries_exceeded_raises(self):
        from anthropic import RateLimitError

        mock_response = MagicMock()
        mock_response.status_code = 429

        func = MagicMock(side_effect=RateLimitError(message="rate limited", response=mock_response, body={}))

        with patch("time.sleep"):
            with pytest.raises(RateLimitError):
                retry_with_backoff(func, max_retries=2, initial_delay=0.01)

        # Initial attempt + 2 retries = 3 calls
        assert func.call_count == 3

    def test_no_retry_on_generic_api_error(self):
        """API errors (non-rate-limit, non-connection) should not retry."""
        from anthropic import APIError

        mock_request = MagicMock()

        func = MagicMock(side_effect=APIError(message="bad request", request=mock_request, body={}))

        with pytest.raises(APIError, match="bad request"):
            retry_with_backoff(func, max_retries=3)

        # Should not retry
        assert func.call_count == 1

    def test_exponential_backoff_delays(self):
        from anthropic import RateLimitError

        mock_response = MagicMock()
        mock_response.status_code = 429

        func = MagicMock(
            side_effect=[
                RateLimitError(message="rate limited", response=mock_response, body={}),
                RateLimitError(message="rate limited", response=mock_response, body={}),
                "success",
            ]
        )

        sleep_calls = []
        with patch("time.sleep", side_effect=lambda x: sleep_calls.append(x)):
            result = retry_with_backoff(func, max_retries=3, initial_delay=1.0, backoff_factor=2.0)

        assert result == "success"
        # First retry: 1.0s, Second retry: 2.0s (1.0 * 2.0)
        assert sleep_calls == [1.0, 2.0]

    def test_returns_result_type(self):
        """Test that return type matches function return type."""
        func = MagicMock(return_value={"key": "value", "count": 42})

        result = retry_with_backoff(func)

        assert result == {"key": "value", "count": 42}
        assert isinstance(result, dict)

    def test_custom_max_retries(self):
        from anthropic import APIConnectionError

        mock_request = MagicMock()

        func = MagicMock(side_effect=APIConnectionError(message="connection failed", request=mock_request))

        with patch("time.sleep"):
            with pytest.raises(APIConnectionError):
                retry_with_backoff(func, max_retries=5, initial_delay=0.01)

        # Initial attempt + 5 retries = 6 calls
        assert func.call_count == 6

    def test_zero_retries(self):
        from anthropic import RateLimitError

        mock_response = MagicMock()
        mock_response.status_code = 429

        func = MagicMock(side_effect=RateLimitError(message="rate limited", response=mock_response, body={}))

        with pytest.raises(RateLimitError):
            retry_with_backoff(func, max_retries=0)

        # Only initial attempt
        assert func.call_count == 1
