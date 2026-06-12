"""Tests for app.features.interview_questions (FR-007)."""

from __future__ import annotations

import json

from app.features.interview_questions import build_prompt, parse_response


def test_build_prompt_includes_jd_and_company_info() -> None:
    prompt = build_prompt(
        job_description="Looking for a backend engineer with cloud experience.",
        company_info="We heavily use Docker and Kubernetes.",
        language="en",
    )
    assert "Looking for a backend engineer with cloud experience." in prompt
    assert "We heavily use Docker and Kubernetes." in prompt


def test_build_prompt_omits_company_section_when_empty() -> None:
    prompt = build_prompt(job_description="Some JD text", company_info="", language="en")
    assert "Company information:" not in prompt


def test_build_prompt_language_instruction_for_telugu() -> None:
    prompt = build_prompt(job_description="Some JD text", company_info="", language="te")
    assert "Respond entirely in Telugu" in prompt


def test_parse_response_valid_json_array() -> None:
    raw = json.dumps(
        [
            {
                "topic": "Technical Skills",
                "questions": ["Explain Docker.", "What is containerization?"],
            },
            {
                "topic": "Behavioral",
                "questions": ["Tell me about a conflict you resolved."],
            },
        ]
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert len(result.groups) == 2
    assert result.groups[0].topic == "Technical Skills"
    assert "Explain Docker." in result.groups[0].questions


def test_parse_response_strips_markdown_code_fence() -> None:
    raw = (
        "```json\n"
        + json.dumps([{"topic": "Domain Knowledge", "questions": ["Explain pandas."]}])
        + "\n```"
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.groups[0].topic == "Domain Knowledge"


def test_parse_response_invalid_json_returns_fallback() -> None:
    result = parse_response("not valid json")

    assert result.is_fallback is True
    assert result.groups == []
    assert result.raw_error is not None


def test_parse_response_skips_group_with_no_valid_questions() -> None:
    raw = json.dumps(
        [
            {"topic": "Good group", "questions": ["Q1?", "Q2?"]},
            {"topic": "Empty questions", "questions": []},
            {"topic": "Non-string questions", "questions": [123, None]},
        ]
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert len(result.groups) == 1
    assert result.groups[0].topic == "Good group"


def test_parse_response_empty_array_returns_fallback() -> None:
    result = parse_response(json.dumps([]))

    assert result.is_fallback is True
    assert result.groups == []
