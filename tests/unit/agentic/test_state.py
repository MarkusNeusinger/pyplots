"""Tests for agentic/workflows/modules/state.py."""

import io
import json
import os

import pytest
from state import WorkflowState


class TestWorkflowStateInit:
    """Tests for WorkflowState construction."""

    def test_creates_with_run_id(self):
        state = WorkflowState(run_id="abc123", prompt="test task")
        assert state.run_id == "abc123"
        assert state.prompt == "test task"

    def test_requires_run_id(self):
        with pytest.raises(ValueError, match="run_id is required"):
            WorkflowState(run_id="", prompt="test")

    def test_default_prompt_is_empty(self):
        state = WorkflowState(run_id="abc123")
        assert state.prompt == ""


class TestWorkflowStateUpdate:
    """Tests for state.update()."""

    def test_updates_core_fields(self):
        state = WorkflowState(run_id="abc123")
        state.update(task_type="bug", plan_file="spec.md")
        assert state.task_type == "bug"
        assert state.plan_file == "spec.md"

    def test_ignores_non_core_fields(self):
        state = WorkflowState(run_id="abc123")
        state.update(unknown_field="value")
        assert state.get("unknown_field") is None

    def test_updates_test_fields(self):
        state = WorkflowState(run_id="abc123")
        state.update(test_passed=True, test_failed_count=0)
        assert state.test_passed is True
        assert state.test_failed_count == 0

    def test_updates_review_fields(self):
        state = WorkflowState(run_id="abc123")
        state.update(review_success=False, review_blocker_count=2)
        assert state.review_success is False
        assert state.review_blocker_count == 2

    def test_updates_document_path(self):
        state = WorkflowState(run_id="abc123")
        state.update(document_path="docs/feature.md")
        assert state.document_path == "docs/feature.md"


class TestWorkflowStateProperties:
    """Tests for state property accessors."""

    def test_properties_return_none_when_unset(self):
        state = WorkflowState(run_id="abc123")
        assert state.task_type is None
        assert state.plan_file is None
        assert state.test_passed is None
        assert state.test_failed_count is None
        assert state.review_success is None
        assert state.review_blocker_count is None
        assert state.document_path is None

    def test_get_with_default(self):
        state = WorkflowState(run_id="abc123")
        assert state.get("missing", "default") == "default"
        assert state.get("run_id") == "abc123"


class TestWorkflowStateSaveLoad:
    """Tests for save() and load() filesystem operations."""

    def test_save_creates_file(self, tmp_path):
        state = WorkflowState(run_id="test123", prompt="hello")
        state.update(task_type="bug")
        path = state.save(str(tmp_path))
        assert os.path.exists(path)
        with open(path) as f:
            data = json.load(f)
        assert data["run_id"] == "test123"
        assert data["task_type"] == "bug"

    def test_save_creates_directory(self, tmp_path):
        state = WorkflowState(run_id="new123")
        path = state.save(str(tmp_path))
        assert os.path.exists(path)

    def test_load_existing_state(self, tmp_path):
        state = WorkflowState(run_id="load123", prompt="test prompt")
        state.update(task_type="feature", plan_file="spec.md")
        state.save(str(tmp_path))

        loaded = WorkflowState.load("load123", str(tmp_path))
        assert loaded is not None
        assert loaded.run_id == "load123"
        assert loaded.prompt == "test prompt"
        assert loaded.task_type == "feature"
        assert loaded.plan_file == "spec.md"

    def test_load_returns_none_for_missing(self, tmp_path):
        result = WorkflowState.load("nonexistent", str(tmp_path))
        assert result is None

    def test_load_returns_none_for_corrupt_json(self, tmp_path):
        state_dir = tmp_path / "agentic" / "runs" / "corrupt"
        state_dir.mkdir(parents=True)
        (state_dir / "state.json").write_text("not valid json")
        result = WorkflowState.load("corrupt", str(tmp_path))
        assert result is None

    def test_roundtrip_preserves_all_fields(self, tmp_path):
        state = WorkflowState(run_id="rt123", prompt="roundtrip")
        state.update(
            task_type="chore",
            plan_file="spec.md",
            test_passed=True,
            test_failed_count=0,
            review_success=True,
            review_blocker_count=0,
            document_path="docs/out.md",
        )
        state.save(str(tmp_path))

        loaded = WorkflowState.load("rt123", str(tmp_path))
        assert loaded.task_type == "chore"
        assert loaded.test_passed is True
        assert loaded.review_success is True
        assert loaded.document_path == "docs/out.md"


class TestWorkflowStateFromStdin:
    """Tests for from_stdin() class method."""

    def test_returns_none_when_tty(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", type("FakeStdin", (), {"isatty": lambda self: True})())
        result = WorkflowState.from_stdin()
        assert result is None

    def test_reads_from_piped_input(self, monkeypatch):
        fake_stdin = io.StringIO(json.dumps({"run_id": "pipe123", "prompt": "piped"}))
        fake_stdin.isatty = lambda: False
        monkeypatch.setattr("sys.stdin", fake_stdin)
        result = WorkflowState.from_stdin()
        assert result is not None
        assert result.run_id == "pipe123"

    def test_returns_none_for_empty_stdin(self, monkeypatch):
        fake_stdin = io.StringIO("")
        fake_stdin.isatty = lambda: False
        monkeypatch.setattr("sys.stdin", fake_stdin)
        result = WorkflowState.from_stdin()
        assert result is None

    def test_returns_none_for_invalid_json(self, monkeypatch):
        fake_stdin = io.StringIO("not json")
        fake_stdin.isatty = lambda: False
        monkeypatch.setattr("sys.stdin", fake_stdin)
        result = WorkflowState.from_stdin()
        assert result is None


class TestWorkflowStateToStdout:
    """Tests for to_stdout() method."""

    def test_outputs_json_to_stdout(self, capsys):
        state = WorkflowState(run_id="out123", prompt="output test")
        state.update(task_type="bug")
        state.to_stdout()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["run_id"] == "out123"
        assert data["task_type"] == "bug"
