"""Tests for app.features.readiness_score (FR-009)."""

from __future__ import annotations

import json

from app.features.readiness_score import (
    NOT_AVAILABLE_REASON,
    build_prompt,
    not_available_result,
    parse_response,
)


def test_not_available_result_when_no_resume() -> None:
    result = not_available_result()

    assert result.is_available is False
    assert result.is_fallback is False
    assert result.score is None
    assert result.not_available_reason == NOT_AVAILABLE_REASON


def test_build_prompt_includes_jd_and_resume() -> None:
    prompt = build_prompt(
        job_description="Looking for a data analyst with SQL and Python.",
        resume_text="Data analyst with 3 years SQL experience, learning Python.",
        language="en",
    )
    assert "Looking for a data analyst with SQL and Python." in prompt
    assert "Data analyst with 3 years SQL experience" in prompt
    assert "technical_match" in prompt
    assert "overall_readiness" in prompt


def test_parse_response_valid_json_object() -> None:
    raw = json.dumps(
        {
            "technical_match": 75,
            "communication_match": 80,
            "domain_match": 60,
            "overall_readiness": 72,
            "commentary": "Solid technical base, domain knowledge needs work.",
        }
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.is_available is True
    assert result.score is not None
    assert result.score.technical_match == 75
    assert result.score.communication_match == 80
    assert result.score.domain_match == 60
    assert result.score.overall_readiness == 72
    assert "Solid technical base" in result.score.commentary


def test_parse_response_strips_markdown_code_fence() -> None:
    raw = (
        "```json\n"
        + json.dumps(
            {
                "technical_match": 50,
                "communication_match": 50,
                "domain_match": 50,
                "overall_readiness": 50,
                "commentary": "",
            }
        )
        + "\n```"
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.score is not None
    assert result.score.overall_readiness == 50


def test_parse_response_coerces_float_scores() -> None:
    raw = json.dumps(
        {
            "technical_match": 75.6,
            "communication_match": 80.0,
            "domain_match": 60.4,
            "overall_readiness": 72.5,
            "commentary": "",
        }
    )

    result = parse_response(raw)

    assert result.is_fallback is False
    assert result.score is not None
    assert result.score.technical_match == 76
    assert result.score.domain_match == 60


def test_parse_response_invalid_json_returns_fallback() -> None:
    result = parse_response("not json")

    assert result.is_fallback is True
    assert result.score is None
    assert result.raw_error is not None


def test_parse_response_out_of_range_score_returns_fallback() -> None:
    raw = json.dumps(
        {
            "technical_match": 150,
            "communication_match": 80,
            "domain_match": 60,
            "overall_readiness": 72,
            "commentary": "",
        }
    )

    result = parse_response(raw)

    assert result.is_fallback is True
    assert result.score is None


def test_parse_response_missing_field_returns_fallback() -> None:
    raw = json.dumps(
        {
            "technical_match": 75,
            "communication_match": 80,
            "domain_match": 60,
            # overall_readiness missing
            "commentary": "",
        }
    )

    result = parse_response(raw)

    assert result.is_fallback is True
    assert result.score is None


def test_parse_response_non_dict_json_returns_fallback() -> None:
    result = parse_response(json.dumps([1, 2, 3]))

    assert result.is_fallback is True
    assert result.score is None
