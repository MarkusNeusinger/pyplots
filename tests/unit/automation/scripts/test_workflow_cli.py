"""Tests for automation.scripts.workflow_cli module."""

import json
import subprocess
import sys


def run_cli(*args: str) -> tuple[int, str]:
    """Run the workflow CLI with given arguments."""
    result = subprocess.run(
        [sys.executable, "-m", "automation.scripts.workflow_cli", *args], capture_output=True, text=True
    )
    return result.returncode, result.stdout.strip()


class TestExtractBranch:
    """Tests for extract-branch command."""

    def test_valid_auto_branch(self):
        code, output = run_cli("extract-branch", "auto/scatter-basic/matplotlib")
        assert code == 0
        data = json.loads(output)
        assert data["spec_id"] == "scatter-basic"
        assert data["library"] == "matplotlib"
        assert data["is_auto_branch"] is True

    def test_invalid_branch(self):
        code, output = run_cli("extract-branch", "feature/something")
        assert code == 1
        assert output == "null"


class TestExtractSubIssue:
    """Tests for extract-sub-issue command."""

    def test_with_sub_issue(self):
        code, output = run_cli("extract-sub-issue", "Sub-Issue: #42")
        assert code == 0
        assert output == "42"

    def test_without_sub_issue(self):
        code, output = run_cli("extract-sub-issue", "No sub-issue here")
        assert code == 1
        assert output == ""


class TestGetAttemptCount:
    """Tests for get-attempt-count command."""

    def test_with_attempt_labels(self):
        code, output = run_cli("get-attempt-count", "ai-attempt-2,library:matplotlib")
        assert code == 0
        assert output == "2"

    def test_without_attempt_labels(self):
        code, output = run_cli("get-attempt-count", "library:matplotlib,testing")
        assert code == 0
        assert output == "0"

    def test_empty_labels(self):
        code, output = run_cli("get-attempt-count", "")
        assert code == 0
        assert output == "0"


class TestParsePlotPath:
    """Tests for parse-plot-path command."""

    def test_valid_path(self):
        code, output = run_cli("parse-plot-path", "plots/matplotlib/scatter/scatter-basic/default.py")
        assert code == 0
        data = json.loads(output)
        assert data["library"] == "matplotlib"
        assert data["spec_id"] == "scatter-basic"
        assert data["variant"] == "default"

    def test_invalid_path(self):
        code, output = run_cli("parse-plot-path", "invalid/path.py")
        assert code == 1
        assert output == "null"


class TestStatusTransition:
    """Tests for status-transition command."""

    def test_simple_transition(self):
        code, output = run_cli("status-transition", "generating,library:matplotlib", "testing")
        assert code == 0
        assert '--remove-label "generating"' in output
        assert '--add-label "testing"' in output

    def test_no_change_needed(self):
        code, output = run_cli("status-transition", "testing", "testing")
        assert code == 0
        assert output == ""


class TestQualityLabel:
    """Tests for quality-label command."""

    def test_excellent(self):
        code, output = run_cli("quality-label", "95")
        assert code == 0
        assert output == "quality:excellent"

    def test_good(self):
        code, output = run_cli("quality-label", "87")
        assert code == 0
        assert output == "quality:good"

    def test_poor(self):
        code, output = run_cli("quality-label", "50")
        assert code == 0
        assert output == "quality:poor"
