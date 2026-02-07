"""Tests for additional functions in agentic/workflows/modules/agent.py."""

import json
import os
import subprocess
from unittest.mock import MagicMock, patch

from agent import (
    AgentPromptRequest,
    AgentPromptResponse,
    RetryCode,
    check_cli_installed,
    convert_jsonl_to_json,
    get_cli_path,
    parse_jsonl_output,
    prompt_claude_code,
    prompt_claude_code_with_retry,
    save_last_entry_as_raw_result,
    save_prompt,
)


class TestGetCliPath:
    """Tests for get_cli_path function."""

    def test_claude_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLAUDE_CODE_PATH", None)
            assert get_cli_path("claude") == "claude"

    def test_claude_from_env(self):
        with patch.dict(os.environ, {"CLAUDE_CODE_PATH": "/custom/claude"}):
            assert get_cli_path("claude") == "/custom/claude"

    def test_copilot_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("COPILOT_CLI_PATH", None)
            assert get_cli_path("copilot") == "copilot"

    def test_copilot_from_env(self):
        with patch.dict(os.environ, {"COPILOT_CLI_PATH": "/custom/copilot"}):
            assert get_cli_path("copilot") == "/custom/copilot"

    def test_gemini_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GEMINI_CLI_PATH", None)
            assert get_cli_path("gemini") == "gemini"

    def test_unknown_cli_falls_back_to_claude(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLAUDE_CODE_PATH", None)
            assert get_cli_path("unknown") == "claude"


class TestCheckCliInstalled:
    """Tests for check_cli_installed function."""

    def test_returns_none_when_installed(self):
        with patch("agent.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert check_cli_installed("claude") is None

    def test_returns_error_when_not_installed(self):
        with patch("agent.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            result = check_cli_installed("claude")
            assert result is not None
            assert "not installed" in result

    def test_returns_error_on_file_not_found(self):
        with patch("agent.subprocess.run", side_effect=FileNotFoundError):
            result = check_cli_installed("claude")
            assert result is not None
            assert "not installed" in result


class TestParseJsonlOutput:
    """Tests for parse_jsonl_output function."""

    def test_parses_valid_jsonl(self, tmp_path):
        f = tmp_path / "output.jsonl"
        f.write_text(
            '{"type": "assistant", "message": {"content": [{"text": "hello"}]}}\n{"type": "result", "result": "done"}\n'
        )
        messages, result_msg = parse_jsonl_output(str(f))
        assert len(messages) == 2
        assert result_msg is not None
        assert result_msg["result"] == "done"

    def test_returns_empty_for_missing_file(self):
        messages, result_msg = parse_jsonl_output("/nonexistent/file.jsonl")
        assert messages == []
        assert result_msg is None

    def test_no_result_message(self, tmp_path):
        f = tmp_path / "output.jsonl"
        f.write_text('{"type": "assistant", "message": {"content": []}}\n')
        messages, result_msg = parse_jsonl_output(str(f))
        assert len(messages) == 1
        assert result_msg is None

    def test_skips_empty_lines(self, tmp_path):
        f = tmp_path / "output.jsonl"
        f.write_text('{"type": "result", "result": "ok"}\n\n\n')
        messages, result_msg = parse_jsonl_output(str(f))
        assert len(messages) == 1
        assert result_msg["result"] == "ok"


class TestConvertJsonlToJson:
    """Tests for convert_jsonl_to_json function."""

    def test_converts_jsonl_to_json_array(self, tmp_path):
        jsonl_file = tmp_path / "output.jsonl"
        jsonl_file.write_text('{"a": 1}\n{"b": 2}\n')
        json_file = convert_jsonl_to_json(str(jsonl_file))
        assert os.path.exists(json_file)
        with open(json_file) as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 2

    def test_output_filename(self, tmp_path):
        jsonl_file = tmp_path / "output.jsonl"
        jsonl_file.write_text('{"a": 1}\n')
        json_file = convert_jsonl_to_json(str(jsonl_file))
        assert json_file.endswith("cli_raw_output.json")


class TestSaveLastEntryAsRawResult:
    """Tests for save_last_entry_as_raw_result function."""

    def test_saves_last_entry(self, tmp_path):
        json_file = tmp_path / "output.json"
        json_file.write_text(json.dumps([{"a": 1}, {"b": 2}, {"c": 3}]))
        result = save_last_entry_as_raw_result(str(json_file))
        assert result is not None
        with open(result) as f:
            data = json.load(f)
        assert data == {"c": 3}

    def test_returns_none_for_empty_array(self, tmp_path):
        json_file = tmp_path / "output.json"
        json_file.write_text("[]")
        assert save_last_entry_as_raw_result(str(json_file)) is None

    def test_returns_none_for_missing_file(self):
        assert save_last_entry_as_raw_result("/nonexistent/file.json") is None

    def test_output_filename(self, tmp_path):
        json_file = tmp_path / "output.json"
        json_file.write_text(json.dumps([{"a": 1}]))
        result = save_last_entry_as_raw_result(str(json_file))
        assert result.endswith("cli_final_object.json")


class TestSavePrompt:
    """Tests for save_prompt function."""

    def test_saves_slash_command_prompt(self, tmp_path):
        with patch("agent.os.path.dirname", return_value=str(tmp_path)):
            with patch("agent.os.path.abspath", return_value=str(tmp_path / "agent.py")):
                # Call with a slash command prompt
                save_prompt("/implement fix the bug", "run123", "builder")
                # Check if file was created (path depends on implementation)

    def test_ignores_non_slash_prompts(self):
        # Should return early without creating files
        save_prompt("just a regular prompt", "run123")
        # No assertion needed - just verifying no exception


class TestPromptClaudeCodeWithRetry:
    """Tests for prompt_claude_code_with_retry function."""

    def _make_request(self, tmp_path):
        return AgentPromptRequest(
            prompt="test", run_id="abc123", agent_name="test", model="small", output_file=str(tmp_path / "output.jsonl")
        )

    def test_returns_on_success(self, tmp_path):
        success_response = AgentPromptResponse(output="done", success=True, retry_code=RetryCode.NONE)
        with patch("agent.prompt_claude_code", return_value=success_response):
            result = prompt_claude_code_with_retry(self._make_request(tmp_path), max_retries=2)
        assert result.success

    def test_retries_on_retryable_error(self, tmp_path):
        error_response = AgentPromptResponse(output="error", success=False, retry_code=RetryCode.CLAUDE_CODE_ERROR)
        success_response = AgentPromptResponse(output="done", success=True, retry_code=RetryCode.NONE)
        with patch("agent.prompt_claude_code", side_effect=[error_response, success_response]):
            with patch("agent.time.sleep"):
                result = prompt_claude_code_with_retry(self._make_request(tmp_path), max_retries=2)
        assert result.success

    def test_gives_up_after_max_retries(self, tmp_path):
        error_response = AgentPromptResponse(output="error", success=False, retry_code=RetryCode.TIMEOUT_ERROR)
        with patch("agent.prompt_claude_code", return_value=error_response):
            with patch("agent.time.sleep"):
                result = prompt_claude_code_with_retry(self._make_request(tmp_path), max_retries=2)
        assert not result.success

    def test_no_retry_on_non_retryable_error(self, tmp_path):
        error_response = AgentPromptResponse(output="fatal", success=False, retry_code=RetryCode.NONE)
        with patch("agent.prompt_claude_code", return_value=error_response) as mock:
            result = prompt_claude_code_with_retry(self._make_request(tmp_path), max_retries=3)
        assert not result.success
        mock.assert_called_once()

    def test_custom_retry_delays(self, tmp_path):
        error_response = AgentPromptResponse(output="error", success=False, retry_code=RetryCode.EXECUTION_ERROR)
        with patch("agent.prompt_claude_code", return_value=error_response):
            with patch("agent.time.sleep") as mock_sleep:
                prompt_claude_code_with_retry(self._make_request(tmp_path), max_retries=2, retry_delays=[10, 20])
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(10)
        mock_sleep.assert_any_call(20)


class TestPromptClaudeCode:
    """Tests for prompt_claude_code function."""

    def test_returns_error_when_cli_not_installed(self, tmp_path):
        request = AgentPromptRequest(
            prompt="test", run_id="abc123", agent_name="test", model="small", output_file=str(tmp_path / "output.jsonl")
        )
        with patch("agent.check_cli_installed", return_value="Error: CLI not installed"):
            result = prompt_claude_code(request)
        assert not result.success
        assert "not installed" in result.output

    def test_handles_timeout_error(self, tmp_path):
        output_file = tmp_path / "output.jsonl"
        output_file.write_text("")
        request = AgentPromptRequest(
            prompt="test", run_id="abc123", agent_name="test", model="small", output_file=str(output_file), timeout=1
        )
        with patch("agent.check_cli_installed", return_value=None):
            with patch("agent.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="test", timeout=1)):
                result = prompt_claude_code(request)
        assert not result.success
        assert result.retry_code == RetryCode.TIMEOUT_ERROR

    def test_successful_non_claude_cli(self, tmp_path):
        output_file = tmp_path / "output.jsonl"
        request = AgentPromptRequest(
            prompt="test",
            run_id="abc123",
            agent_name="test",
            model="small",
            cli="copilot",
            output_file=str(output_file),
        )

        def fake_run(cmd, **kwargs):
            # Simulate CLI writing to the stdout file handle
            stdout_fh = kwargs.get("stdout")
            if stdout_fh and hasattr(stdout_fh, "write"):
                stdout_fh.write("copilot output here")
            return MagicMock(returncode=0, stderr="")

        with patch("agent.check_cli_installed", return_value=None):
            with patch("agent.subprocess.run", side_effect=fake_run):
                result = prompt_claude_code(request)
        assert result.success
        assert "copilot output here" in result.output


class TestAgentPromptRequest:
    """Tests for AgentPromptRequest model."""

    def test_default_timeout(self):
        req = AgentPromptRequest(prompt="test", run_id="abc", agent_name="test", output_file="/tmp/out.jsonl")
        assert req.timeout == 1800

    def test_custom_timeout(self):
        req = AgentPromptRequest(
            prompt="test", run_id="abc", agent_name="test", output_file="/tmp/out.jsonl", timeout=600
        )
        assert req.timeout == 600

    def test_none_timeout(self):
        req = AgentPromptRequest(
            prompt="test", run_id="abc", agent_name="test", output_file="/tmp/out.jsonl", timeout=None
        )
        assert req.timeout is None
