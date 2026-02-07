"""Tests for agentic/workflows/modules/template.py."""

import pytest
from template import load_template, render_template


class TestLoadTemplate:
    """Tests for load_template function."""

    def test_loads_existing_file(self, tmp_path):
        template_file = tmp_path / "cmds" / "test.md"
        template_file.parent.mkdir(parents=True)
        template_file.write_text("Hello $1")
        result = load_template("cmds/test.md", str(tmp_path))
        assert result == "Hello $1"

    def test_raises_for_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="Template not found"):
            load_template("nonexistent.md", str(tmp_path))


class TestRenderTemplate:
    """Tests for render_template function."""

    def test_replaces_positional_vars(self):
        result = render_template("Hello $1, meet $2", {"1": "Alice", "2": "Bob"})
        assert result == "Hello Alice, meet Bob"

    def test_replaces_arguments_var(self):
        result = render_template("Task: $ARGUMENTS", {"ARGUMENTS": "fix the bug"})
        assert result == "Task: fix the bug"

    def test_ignores_non_digit_non_arguments_keys(self):
        result = render_template("Hello $name", {"name": "Alice"})
        assert result == "Hello $name"

    def test_handles_no_variables(self):
        result = render_template("No vars here", {})
        assert result == "No vars here"

    def test_multiple_occurrences(self):
        result = render_template("$1 and $1 again", {"1": "X"})
        assert result == "X and X again"

    def test_mixed_positional_and_arguments(self):
        result = render_template("Run $1: $ARGUMENTS", {"1": "abc", "ARGUMENTS": "do stuff"})
        assert result == "Run abc: do stuff"
