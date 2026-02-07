"""Tests for resolve_state in agentic/workflows/modules/state.py."""

import io
import json
from unittest.mock import MagicMock

import pytest
from state import WorkflowState, resolve_state


class TestResolveState:
    """Tests for resolve_state function."""

    def test_loads_from_run_id(self, tmp_path):
        # Create state file
        state = WorkflowState(run_id="abc123", prompt="test")
        state.update(task_type="bug")
        state.save(str(tmp_path))

        console = MagicMock()
        result = resolve_state("abc123", str(tmp_path), console)
        assert result.run_id == "abc123"
        assert result.task_type == "bug"

    def test_exits_when_run_id_not_found(self, tmp_path):
        console = MagicMock()
        with pytest.raises(SystemExit):
            resolve_state("nonexistent", str(tmp_path), console)

    def test_loads_from_stdin(self, tmp_path, monkeypatch):
        fake_stdin = io.StringIO(json.dumps({"run_id": "pipe123", "prompt": "piped"}))
        fake_stdin.isatty = lambda: False
        monkeypatch.setattr("sys.stdin", fake_stdin)

        console = MagicMock()
        result = resolve_state(None, str(tmp_path), console)
        assert result.run_id == "pipe123"

    def test_creates_from_plan_file(self, tmp_path, monkeypatch):
        # Make stdin appear as tty so from_stdin returns None
        fake_stdin = MagicMock()
        fake_stdin.isatty.return_value = True
        monkeypatch.setattr("sys.stdin", fake_stdin)

        console = MagicMock()
        result = resolve_state(None, str(tmp_path), console, plan_file="spec.md")
        assert result is not None
        assert result.plan_file == "spec.md"
        assert result.prompt == "(from plan file)"

    def test_exits_when_no_source(self, tmp_path, monkeypatch):
        fake_stdin = MagicMock()
        fake_stdin.isatty.return_value = True
        monkeypatch.setattr("sys.stdin", fake_stdin)

        console = MagicMock()
        with pytest.raises(SystemExit):
            resolve_state(None, str(tmp_path), console)

    def test_shows_usage_hint_on_error(self, tmp_path, monkeypatch):
        fake_stdin = MagicMock()
        fake_stdin.isatty.return_value = True
        monkeypatch.setattr("sys.stdin", fake_stdin)

        console = MagicMock()
        with pytest.raises(SystemExit):
            resolve_state(None, str(tmp_path), console, usage_hint="try this instead")
        # Check that usage hint was printed
        printed = " ".join(str(c) for c in console.print.call_args_list)
        assert "try this instead" in printed


class TestWorkflowStateAdditionalProperties:
    """Tests for commit_message and pr_url properties."""

    def test_commit_message_property(self):
        state = WorkflowState(run_id="abc123")
        assert state.commit_message is None
        state.update(commit_message="feat: add feature")
        assert state.commit_message == "feat: add feature"

    def test_pr_url_property(self):
        state = WorkflowState(run_id="abc123")
        assert state.pr_url is None
        state.update(pr_url="https://github.com/org/repo/pull/1")
        assert state.pr_url == "https://github.com/org/repo/pull/1"

    def test_save_with_phase(self, tmp_path):
        state = WorkflowState(run_id="abc123")
        path = state.save(str(tmp_path), phase="ship")
        assert path.endswith("state.json")

    def test_classify_reason_property(self):
        state = WorkflowState(run_id="abc123")
        state.update(classify_reason="Looks like a bug fix")
        assert state.get("classify_reason") == "Looks like a bug fix"
