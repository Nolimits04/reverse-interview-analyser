"""Tests for app.features.gap_analysis (FR-008)."""

from __future__ import annotations

import json

from app.features.gap_analysis import (
    NOT_AVAILABLE_REASON,
    build_prompt,
    not_available_result,
    parse_response,
)


def test_not_available_result_when_no_resume() -> None:
    result = not_available_result()

    assert result.is_available is False
    assert result.is_fallback is False
    assert result.items == []
    assert result.not_available_reason == NOT_AVAILABLE_REASON


def test_build_prompt_includes_jd_and_resume() -> None:
    prompt = build_prompt(
        job_description="Looking for a Python developer with AWS experience.",
        resume_text="Experienced Python developer, 5 years, no cloud experience.",
        language="en",
    )
    assert "Looking for a Python developer with AWS experience." in prompt
    assert "Experienced Python developer, 5 years" in prompt


def test_build_prompt_language_instruction_for_hindi() -> None:
    prompt = build_prompt(job_description="JD", resume_text="Resume", language="hi")
    assert "Respond entirely in Hindi" in prompt
    assert "strong_match" in prompt
    assert "weak_match" in prompt
    assert "missing" in prompt


def test_parse_response_valid_json_array() -> None:
    raw = json.dumps(
        [
            {"requirement": "Python", "category": "strong_match", "note": "5 years exp"},
            {"requirement": "AWS", "category": "missing", "note": "Not mentioned"},
            {"requirement": "Docker", "category": "weak_match", "note": "Basic only"},
        ]
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.is_available is True
    assert len(result.items) == 3
    categories = {item.requirement: item.category for item in result.items}
    assert categories["Python"] == "strong_match"
    assert categories["AWS"] == "missing"
    assert categories["Docker"] == "weak_match"


def test_parse_response_strips_markdown_code_fence() -> None:
    raw = (
        "```json\n"
        + json.dumps([{"requirement": "SQL", "category": "strong_match", "note": ""}])
        + "\n```"
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.items[0].requirement == "SQL"


def test_parse_response_invalid_category_skipped() -> None:
    raw = json.dumps(
        [
            {"requirement": "Python", "category": "strong_match", "note": ""},
            {"requirement": "Bad category", "category": "not_a_real_category", "note": ""},
        ]
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert len(result.items) == 1
    assert result.items[0].requirement == "Python"


def test_parse_response_invalid_json_returns_fallback() -> None:
    result = parse_response("not json")

    assert result.is_fallback is True
    assert result.items == []
    assert result.raw_error is not None


def test_parse_response_missing_note_defaults_to_empty_string() -> None:
    raw = json.dumps([{"requirement": "Python", "category": "strong_match"}])

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.items[0].note == ""
