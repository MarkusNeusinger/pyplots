"""Tests for run_phase in agentic/workflows/modules/orchestrator.py."""

from unittest.mock import MagicMock, patch

from orchestrator import run_phase


class TestRunPhase:
    """Tests for run_phase function."""

    def test_returns_exit_code_and_empty_stdout(self):
        mock_result = MagicMock(returncode=0)
        console = MagicMock()
        with patch("orchestrator.subprocess.run", return_value=mock_result):
            rc, stdout = run_phase("plan.py", ["arg"], console, "Plan")
        assert rc == 0
        assert stdout == ""

    def test_captures_stdout_when_requested(self):
        mock_result = MagicMock(returncode=0, stdout='{"run_id": "abc"}')
        console = MagicMock()
        with patch("orchestrator.subprocess.run", return_value=mock_result):
            rc, stdout = run_phase("plan.py", ["arg"], console, "Plan", capture_stdout=True)
        assert rc == 0
        assert '"run_id"' in stdout

    def test_returns_nonzero_on_failure(self):
        mock_result = MagicMock(returncode=1)
        console = MagicMock()
        with patch("orchestrator.subprocess.run", return_value=mock_result):
            rc, _ = run_phase("build.py", [], console, "Build")
        assert rc == 1

    def test_prints_command(self):
        mock_result = MagicMock(returncode=0)
        console = MagicMock()
        with patch("orchestrator.subprocess.run", return_value=mock_result):
            run_phase("test.py", ["--run-id", "abc"], console, "Test")
        console.print.assert_called()

    def test_passes_args_to_subprocess(self):
        mock_result = MagicMock(returncode=0)
        console = MagicMock()
        with patch("orchestrator.subprocess.run", return_value=mock_result) as mock_run:
            run_phase("plan.py", ["--model", "large"], console, "Plan")
        cmd = mock_run.call_args[0][0]
        assert "--model" in cmd
        assert "large" in cmd
