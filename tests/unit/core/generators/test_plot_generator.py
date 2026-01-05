"""Tests for core.generators.plot_generator module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.generators.plot_generator import (
    extract_and_validate_code,
    generate_code,
    load_generation_rules,
    load_quality_criteria,
    load_self_review_checklist,
    load_spec,
    retry_with_backoff,
    save_implementation,
)


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


class TestLoadSpec:
    """Tests for load_spec function."""

    def test_load_spec_file_not_found(self):
        """Should raise FileNotFoundError for missing spec."""
        with pytest.raises(FileNotFoundError, match="Spec file not found"):
            load_spec("nonexistent-spec-id")

    def test_load_spec_success(self, tmp_path: Path, monkeypatch):
        """Should load spec content from file."""
        # Create a mock spec file
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        spec_file = specs_dir / "test-spec.md"
        spec_content = """# Test Spec

**Spec Version:** 1.0.0

Description of the test spec.
"""
        spec_file.write_text(spec_content)

        # Change to tmp directory so relative path works
        monkeypatch.chdir(tmp_path)

        result = load_spec("test-spec")

        assert "# Test Spec" in result
        assert "**Spec Version:** 1.0.0" in result

    def test_load_spec_without_version(self, tmp_path: Path, monkeypatch, capsys):
        """Should warn when spec has no version marker."""
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        spec_file = specs_dir / "no-version-spec.md"
        spec_file.write_text("# Spec without version\n\nSome content.")

        monkeypatch.chdir(tmp_path)

        result = load_spec("no-version-spec")

        assert "# Spec without version" in result
        captured = capsys.readouterr()
        assert "Warning: Spec has no version marker" in captured.out


class TestLoadGenerationRules:
    """Tests for load_generation_rules function."""

    def test_load_generation_rules_file_not_found(self):
        """Should raise FileNotFoundError for missing rules."""
        with pytest.raises(FileNotFoundError, match="Rules not found"):
            load_generation_rules("nonexistent-version")

    def test_load_generation_rules_success(self, tmp_path: Path, monkeypatch):
        """Should load generation rules from file."""
        rules_dir = tmp_path / "rules" / "generation" / "v1.0.0"
        rules_dir.mkdir(parents=True)
        rules_file = rules_dir / "code-generation-rules.md"
        rules_content = "# Code Generation Rules\n\n- Rule 1\n- Rule 2"
        rules_file.write_text(rules_content)

        monkeypatch.chdir(tmp_path)

        result = load_generation_rules("v1.0.0")

        assert "# Code Generation Rules" in result
        assert "Rule 1" in result


class TestLoadQualityCriteria:
    """Tests for load_quality_criteria function."""

    def test_load_quality_criteria_file_not_found(self):
        """Should raise FileNotFoundError for missing criteria."""
        with pytest.raises(FileNotFoundError, match="Quality criteria not found"):
            load_quality_criteria("nonexistent-version")

    def test_load_quality_criteria_success(self, tmp_path: Path, monkeypatch):
        """Should load quality criteria from file."""
        criteria_dir = tmp_path / "rules" / "generation" / "v2.0.0"
        criteria_dir.mkdir(parents=True)
        criteria_file = criteria_dir / "quality-criteria.md"
        criteria_content = "# Quality Criteria\n\n## Visual Quality\n- Criterion 1"
        criteria_file.write_text(criteria_content)

        monkeypatch.chdir(tmp_path)

        result = load_quality_criteria("v2.0.0")

        assert "# Quality Criteria" in result
        assert "Visual Quality" in result


class TestLoadSelfReviewChecklist:
    """Tests for load_self_review_checklist function."""

    def test_load_self_review_checklist_file_not_found(self):
        """Should raise FileNotFoundError for missing checklist."""
        with pytest.raises(FileNotFoundError, match="Self-review checklist not found"):
            load_self_review_checklist("nonexistent-version")

    def test_load_self_review_checklist_success(self, tmp_path: Path, monkeypatch):
        """Should load self-review checklist from file."""
        checklist_dir = tmp_path / "rules" / "generation" / "v3.0.0"
        checklist_dir.mkdir(parents=True)
        checklist_file = checklist_dir / "self-review-checklist.md"
        checklist_content = "# Self-Review Checklist\n\n- [ ] Check 1\n- [ ] Check 2"
        checklist_file.write_text(checklist_content)

        monkeypatch.chdir(tmp_path)

        result = load_self_review_checklist("v3.0.0")

        assert "# Self-Review Checklist" in result
        assert "Check 1" in result


class TestSaveImplementation:
    """Tests for save_implementation function."""

    def test_save_implementation_creates_directory(self, tmp_path: Path, monkeypatch):
        """Should create directory structure and save file."""
        monkeypatch.chdir(tmp_path)

        result_dict = {
            "code": "import matplotlib.pyplot as plt\nplt.plot([1, 2, 3])\nplt.savefig('plot.png')",
            "file_path": "plots/matplotlib/scatter/scatter-basic/default.py",
        }

        saved_path = save_implementation(result_dict)

        assert saved_path.exists()
        assert saved_path.read_text() == result_dict["code"]
        assert saved_path == Path("plots/matplotlib/scatter/scatter-basic/default.py")

    def test_save_implementation_overwrites_existing(self, tmp_path: Path, monkeypatch):
        """Should overwrite existing file."""
        monkeypatch.chdir(tmp_path)

        # Create existing file
        file_path = tmp_path / "plots" / "test" / "impl.py"
        file_path.parent.mkdir(parents=True)
        file_path.write_text("old code")

        result_dict = {"code": "new code", "file_path": "plots/test/impl.py"}

        save_implementation(result_dict)

        assert file_path.read_text() == "new code"

    def test_save_implementation_returns_path(self, tmp_path: Path, monkeypatch):
        """Should return Path object."""
        monkeypatch.chdir(tmp_path)

        result_dict = {"code": "code", "file_path": "output/file.py"}

        result = save_implementation(result_dict)

        assert isinstance(result, Path)
        assert result == Path("output/file.py")


class TestGenerateCode:
    """Tests for generate_code function."""

    @pytest.fixture
    def mock_files(self, tmp_path: Path, monkeypatch):
        """Set up mock files for generate_code."""
        monkeypatch.chdir(tmp_path)

        # Create specs directory
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        spec_file = specs_dir / "scatter-basic.md"
        spec_file.write_text("# Scatter Basic\n\n**Spec Version:** 1.0.0\n\nA basic scatter plot.")

        # Create rules directory
        rules_dir = tmp_path / "rules" / "generation" / "v1.0.0-draft"
        rules_dir.mkdir(parents=True)
        (rules_dir / "code-generation-rules.md").write_text("# Rules\n\n- Rule 1")
        (rules_dir / "quality-criteria.md").write_text("# Quality\n\n- Criterion 1")
        (rules_dir / "self-review-checklist.md").write_text("# Checklist\n\n- [ ] Check 1")

        return tmp_path

    def test_generate_code_missing_api_key(self, mock_files, monkeypatch):
        """Should raise ValueError when ANTHROPIC_API_KEY is not set."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable not set"):
            generate_code("scatter-basic", "matplotlib")

    def test_generate_code_passes_on_first_attempt(self, mock_files, monkeypatch):
        """Should return result when self-review passes on first attempt."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_code = """import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42)
x = np.random.randn(100)
plt.scatter(x, x)
plt.savefig('plot.png')"""

        mock_review = """## Review Results
✅ PASS: All criteria met

## Verdict
PASS"""

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=f"```python\n{mock_code}\n```")]

        mock_review_message = MagicMock()
        mock_review_message.content = [MagicMock(text=mock_review)]

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [mock_message, mock_review_message]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "matplotlib")

        assert result["passed_review"] is True
        assert result["attempt_count"] == 1
        assert "import matplotlib" in result["code"]
        assert "plots/matplotlib/scatter/scatter-basic/default.py" in result["file_path"]

    def test_generate_code_fails_then_passes(self, mock_files, monkeypatch):
        """Should retry and pass on second attempt after failure."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_code_v1 = "import matplotlib.pyplot as plt\nprint('v1')"
        mock_code_v2 = "import matplotlib.pyplot as plt\nprint('v2')"

        mock_review_fail = """## Review Results
❌ FAIL: Missing plot

## Verdict
FAIL

## Improvements Needed
- Add actual plot code"""

        mock_review_pass = """## Verdict
PASS"""

        mock_msg_v1 = MagicMock()
        mock_msg_v1.content = [MagicMock(text=f"```python\n{mock_code_v1}\n```")]

        mock_msg_v2 = MagicMock()
        mock_msg_v2.content = [MagicMock(text=f"```python\n{mock_code_v2}\n```")]

        mock_review_fail_msg = MagicMock()
        mock_review_fail_msg.content = [MagicMock(text=mock_review_fail)]

        mock_review_pass_msg = MagicMock()
        mock_review_pass_msg.content = [MagicMock(text=mock_review_pass)]

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [mock_msg_v1, mock_review_fail_msg, mock_msg_v2, mock_review_pass_msg]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "matplotlib", max_attempts=3)

        assert result["passed_review"] is True
        assert result["attempt_count"] == 2
        assert "v2" in result["code"]

    def test_generate_code_max_attempts_exhausted(self, mock_files, monkeypatch):
        """Should return failed result after max attempts."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_code = "import matplotlib.pyplot as plt"
        mock_review_fail = "## Verdict\nFAIL"

        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=f"```python\n{mock_code}\n```")]

        mock_review_msg = MagicMock()
        mock_review_msg.content = [MagicMock(text=mock_review_fail)]

        mock_client = MagicMock()
        # Each attempt: 1 generate + 1 review = 2 calls per attempt
        mock_client.messages.create.side_effect = [mock_msg, mock_review_msg, mock_msg, mock_review_msg]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "matplotlib", max_attempts=2)

        assert result["passed_review"] is False
        assert result["attempt_count"] == 2

    def test_generate_code_code_extraction_fails_then_succeeds(self, mock_files, monkeypatch):
        """Should retry when code extraction fails."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_bad_code = "def broken("  # Invalid syntax
        mock_good_code = "import matplotlib.pyplot as plt\nprint('ok')"
        mock_review_pass = "## Verdict\nPASS"

        mock_bad_msg = MagicMock()
        mock_bad_msg.content = [MagicMock(text=f"```python\n{mock_bad_code}\n```")]

        mock_good_msg = MagicMock()
        mock_good_msg.content = [MagicMock(text=f"```python\n{mock_good_code}\n```")]

        mock_review_msg = MagicMock()
        mock_review_msg.content = [MagicMock(text=mock_review_pass)]

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [mock_bad_msg, mock_good_msg, mock_review_msg]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "matplotlib", max_attempts=3)

        assert result["passed_review"] is True
        assert result["attempt_count"] == 2

    def test_generate_code_different_libraries(self, mock_files, monkeypatch):
        """Should generate correct file paths for different libraries."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_code = "import seaborn as sns"
        mock_review = "## Verdict\nPASS"

        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=f"```python\n{mock_code}\n```")]

        mock_review_msg = MagicMock()
        mock_review_msg.content = [MagicMock(text=mock_review)]

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [mock_msg, mock_review_msg]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "seaborn")

        assert "seaborn/scatterplot" in result["file_path"]

    def test_generate_code_with_custom_variant(self, mock_files, monkeypatch):
        """Should include variant in file path."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_code = "import matplotlib.pyplot as plt"
        mock_review = "Verdict: PASS"

        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=f"```python\n{mock_code}\n```")]

        mock_review_msg = MagicMock()
        mock_review_msg.content = [MagicMock(text=mock_review)]

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [mock_msg, mock_review_msg]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "matplotlib", variant="dark-theme")

        assert "dark-theme.py" in result["file_path"]

    def test_generate_code_plotly_library(self, mock_files, monkeypatch):
        """Should handle plotly library mapping."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_code = "import plotly.express as px"
        mock_review = "## Verdict\nPASS"

        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=f"```python\n{mock_code}\n```")]

        mock_review_msg = MagicMock()
        mock_review_msg.content = [MagicMock(text=mock_review)]

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [mock_msg, mock_review_msg]

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            result = generate_code("scatter-basic", "plotly")

        assert "plotly/scatter" in result["file_path"]

    def test_generate_code_extraction_fails_all_attempts(self, mock_files, monkeypatch):
        """Should raise ValueError when code extraction fails on all attempts."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_bad_code = "def broken("  # Invalid syntax

        mock_bad_msg = MagicMock()
        mock_bad_msg.content = [MagicMock(text=f"```python\n{mock_bad_code}\n```")]

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_bad_msg

        with patch("core.generators.plot_generator.anthropic.Anthropic", return_value=mock_client):
            with pytest.raises(ValueError, match="syntax errors"):
                generate_code("scatter-basic", "matplotlib", max_attempts=2)
