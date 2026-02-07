"""Tests for utility functions in agentic/workflows/modules/agent.py."""

import os

from agent import build_cli_command, generate_short_id, get_safe_subprocess_env, truncate_output


class TestBuildCliCommand:
    """Tests for build_cli_command function."""

    def test_claude_basic(self):
        cmd = build_cli_command("claude", "/usr/bin/claude", "hello", "sonnet", False)
        assert cmd[0] == "/usr/bin/claude"
        assert "-p" in cmd
        assert "hello" in cmd
        assert "--model" in cmd
        assert "sonnet" in cmd
        assert "--output-format" in cmd
        assert "stream-json" in cmd
        assert "--verbose" in cmd
        assert "--dangerously-skip-permissions" not in cmd

    def test_claude_with_skip_permissions(self):
        cmd = build_cli_command("claude", "claude", "test", "haiku", True)
        assert "--dangerously-skip-permissions" in cmd

    def test_claude_with_mcp_config(self):
        cmd = build_cli_command("claude", "claude", "test", "haiku", False, "/path/.mcp.json")
        assert "--mcp-config" in cmd
        assert "/path/.mcp.json" in cmd

    def test_copilot_basic(self):
        cmd = build_cli_command("copilot", "copilot", "hello", "model", False)
        assert cmd[0] == "copilot"
        assert "-p" in cmd
        assert "--model" not in cmd
        assert "--verbose" not in cmd

    def test_copilot_skip_permissions(self):
        cmd = build_cli_command("copilot", "copilot", "test", "model", True)
        assert "--allow-all" in cmd

    def test_copilot_mcp_config(self):
        cmd = build_cli_command("copilot", "copilot", "test", "model", False, "/path/.mcp.json")
        assert "--additional-mcp-config" in cmd

    def test_gemini_basic(self):
        cmd = build_cli_command("gemini", "gemini", "hello", "model", False)
        assert cmd == ["gemini", "-p", "hello"]

    def test_unknown_cli_fallback(self):
        cmd = build_cli_command("unknown", "unknown", "hello", "model", False)
        assert cmd == ["unknown", "-p", "hello"]


class TestGetSafeSubprocessEnv:
    """Tests for get_safe_subprocess_env function."""

    def test_returns_dict(self):
        env = get_safe_subprocess_env()
        assert isinstance(env, dict)

    def test_includes_path(self):
        env = get_safe_subprocess_env()
        assert "PATH" in env

    def test_includes_pythonunbuffered(self):
        env = get_safe_subprocess_env()
        assert env.get("PYTHONUNBUFFERED") == "1"

    def test_includes_pwd(self):
        env = get_safe_subprocess_env()
        assert "PWD" in env
        assert env["PWD"] == os.getcwd()

    def test_filters_out_none_values(self):
        env = get_safe_subprocess_env()
        assert all(v is not None for v in env.values())


class TestTruncateOutput:
    """Tests for truncate_output function."""

    def test_short_output_unchanged(self):
        result = truncate_output("short", max_length=100)
        assert result == "short"

    def test_long_output_truncated(self):
        long_text = "a" * 600
        result = truncate_output(long_text, max_length=500)
        assert len(result) <= 500
        assert result.endswith("... (truncated)")

    def test_custom_suffix(self):
        long_text = "x" * 200
        result = truncate_output(long_text, max_length=50, suffix="...")
        assert result.endswith("...")

    def test_jsonl_result_extraction(self):
        """Should extract result text from JSONL data."""
        lines = [
            '{"type": "assistant", "message": {"content": [{"text": "working"}]}}',
            '{"type": "result", "result": "final output"}',
        ]
        jsonl = "\n".join(lines)
        result = truncate_output(jsonl)
        assert "final output" in result


class TestGenerateShortId:
    """Tests for generate_short_id function."""

    def test_returns_8_char_string(self):
        result = generate_short_id()
        assert isinstance(result, str)
        assert len(result) == 8

    def test_unique_ids(self):
        ids = {generate_short_id() for _ in range(100)}
        assert len(ids) == 100
