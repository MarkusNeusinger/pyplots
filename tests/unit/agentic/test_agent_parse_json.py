"""Tests for parse_json() in agentic/workflows/modules/agent.py."""

import json

import pytest
from agent import parse_json
from pydantic import BaseModel


class SampleModel(BaseModel):
    name: str
    value: int


class TestParseJsonDirectParse:
    """Strategy 1: Direct JSON parsing."""

    def test_parses_plain_json_object(self):
        result = parse_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parses_plain_json_array(self):
        result = parse_json("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_parses_with_whitespace(self):
        result = parse_json('  {"key": "value"}  ')
        assert result == {"key": "value"}

    def test_validates_against_target_type(self):
        result = parse_json('{"name": "test", "value": 42}', SampleModel)
        assert isinstance(result, SampleModel)
        assert result.name == "test"
        assert result.value == 42

    def test_validates_array_against_target_type(self):
        data = json.dumps([{"name": "a", "value": 1}, {"name": "b", "value": 2}])
        result = parse_json(data, SampleModel)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, SampleModel) for item in result)


class TestParseJsonMarkdownFences:
    """Strategy 2: Stripping markdown code fences."""

    def test_parses_json_in_code_fence(self):
        output = '```json\n{"key": "value"}\n```'
        result = parse_json(output)
        assert result == {"key": "value"}

    def test_parses_json_in_plain_code_fence(self):
        output = '```\n{"key": "value"}\n```'
        result = parse_json(output)
        assert result == {"key": "value"}

    def test_handles_text_around_fences(self):
        output = 'Here is the result:\n```json\n{"key": "value"}\n```\nDone.'
        result = parse_json(output)
        assert result == {"key": "value"}

    def test_validates_fenced_json_against_type(self):
        output = '```json\n{"name": "test", "value": 42}\n```'
        result = parse_json(output, SampleModel)
        assert isinstance(result, SampleModel)

    def test_fenced_array(self):
        output = "```json\n[1, 2, 3]\n```"
        result = parse_json(output)
        assert result == [1, 2, 3]


class TestParseJsonFindInText:
    """Strategy 3: Find first JSON object or array in text."""

    def test_finds_object_in_surrounding_text(self):
        output = 'The result is {"key": "value"} as expected.'
        result = parse_json(output)
        assert result == {"key": "value"}

    def test_finds_array_in_surrounding_text(self):
        output = "Results: [1, 2, 3] end."
        result = parse_json(output)
        assert result == [1, 2, 3]

    def test_validates_found_json_against_type(self):
        output = 'Output: {"name": "found", "value": 99} done.'
        result = parse_json(output, SampleModel)
        assert isinstance(result, SampleModel)
        assert result.value == 99


class TestParseJsonErrors:
    """Tests for error handling."""

    def test_raises_for_no_json(self):
        with pytest.raises(json.JSONDecodeError, match="No valid JSON found"):
            parse_json("no json here at all")

    def test_raises_for_empty_string(self):
        with pytest.raises(json.JSONDecodeError):
            parse_json("")

    def test_raises_for_only_text(self):
        with pytest.raises(json.JSONDecodeError):
            parse_json("just some plain text without any brackets")
