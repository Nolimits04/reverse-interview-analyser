"""Tests for app.features.hidden_skills (FR-006)."""

from __future__ import annotations

import json

from app.features.hidden_skills import build_prompt, parse_response


def test_build_prompt_includes_jd_and_company_info() -> None:
    prompt = build_prompt(
        job_description="Looking for a Python developer with good communication skills.",
        company_info="We build cloud infrastructure tools.",
        language="en",
    )
    assert "Looking for a Python developer" in prompt
    assert "We build cloud infrastructure tools." in prompt
    assert "Respond entirely in English" in prompt


def test_build_prompt_omits_company_section_when_empty() -> None:
    prompt = build_prompt(job_description="Some JD text", company_info="", language="en")
    assert "Company information:" not in prompt


def test_build_prompt_language_instruction_for_hindi() -> None:
    prompt = build_prompt(job_description="Some JD text", company_info="", language="hi")
    assert "Respond entirely in Hindi" in prompt


def test_parse_response_valid_json_array() -> None:
    raw = json.dumps(
        [
            {
                "explicit_requirement": "Python",
                "hidden_requirement": "Debugging ability",
            },
            {
                "explicit_requirement": "Communication",
                "hidden_requirement": "Stakeholder management",
            },
        ]
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert len(result.rows) == 2
    assert result.rows[0].explicit_requirement == "Python"
    assert result.rows[0].hidden_requirement == "Debugging ability"


def test_parse_response_strips_markdown_code_fence() -> None:
    raw = (
        "```json\n"
        + json.dumps([{"explicit_requirement": "SQL", "hidden_requirement": "Data modeling"}])
        + "\n```"
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.rows[0].explicit_requirement == "SQL"


def test_parse_response_invalid_json_returns_fallback() -> None:
    result = parse_response("not json at all")

    assert result.is_fallback is True
    assert result.rows == []
    assert result.raw_error is not None


def test_parse_response_non_list_json_returns_fallback() -> None:
    result = parse_response(json.dumps({"not": "a list"}))

    assert result.is_fallback is True
    assert result.rows == []


def test_parse_response_skips_malformed_rows() -> None:
    raw = json.dumps(
        [
            {"explicit_requirement": "Python", "hidden_requirement": "Debugging"},
            {"explicit_requirement": "Missing hidden field"},
            "not even a dict",
        ]
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert len(result.rows) == 1
    assert result.rows[0].explicit_requirement == "Python"


def test_parse_response_empty_list_returns_fallback() -> None:
    result = parse_response(json.dumps([]))

    assert result.is_fallback is True
    assert result.rows == []
