"""Tests for agentic/workflows/modules/orchestrator.py."""

import json

from orchestrator import WORKFLOWS_DIR, extract_run_id


class TestExtractRunId:
    """Tests for extract_run_id function."""

    def test_extracts_run_id_from_valid_json(self):
        data = json.dumps({"run_id": "abc12345", "prompt": "test"})
        assert extract_run_id(data) == "abc12345"

    def test_returns_none_for_missing_run_id(self):
        data = json.dumps({"prompt": "test"})
        assert extract_run_id(data) is None

    def test_returns_none_for_invalid_json(self):
        assert extract_run_id("not json") is None

    def test_returns_none_for_empty_string(self):
        assert extract_run_id("") is None

    def test_handles_whitespace_padding(self):
        data = f"  {json.dumps({'run_id': 'xyz789'})}  \n"
        assert extract_run_id(data) == "xyz789"

    def test_returns_none_for_truncated_json(self):
        assert extract_run_id('{"run_id": "abc') is None


class TestWorkflowsDir:
    """Tests for WORKFLOWS_DIR constant."""

    def test_points_to_workflows_directory(self):
        assert WORKFLOWS_DIR.endswith("agentic/workflows") or WORKFLOWS_DIR.endswith("agentic\\workflows")
