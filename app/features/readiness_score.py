"""Interview Readiness Score (FR-009).

Produces an Interview Readiness Score with technical, communication,
domain, and overall percentages plus brief commentary.

Per the spec edge case, if no resume is provided, this module returns a
sentinel "not available" result rather than calling the LLM (mirrors
`gap_analysis`, since the score depends on the resume).
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.i18n.prompts import language_instruction

NOT_AVAILABLE_REASON = "No resume was provided, so an interview readiness score is not available."


@dataclass(frozen=True)
class ReadinessScore:
    """Interview readiness percentages and commentary."""

    technical_match: int
    communication_match: int
    domain_match: int
    overall_readiness: int
    commentary: str = ""


@dataclass(frozen=True)
class ReadinessScoreResult:
    """Result of the interview readiness score generation."""

    score: ReadinessScore | None
    raw_error: str | None = None
    not_available_reason: str | None = None

    @property
    def is_fallback(self) -> bool:
        """True if this result is a fallback/error placeholder."""
        return self.raw_error is not None

    @property
    def is_available(self) -> bool:
        """True if a score was actually produced."""
        return self.not_available_reason is None and self.raw_error is None


def not_available_result() -> ReadinessScoreResult:
    """Return the sentinel result used when no resume was provided."""
    return ReadinessScoreResult(score=None, not_available_reason=NOT_AVAILABLE_REASON)


def build_prompt(job_description: str, resume_text: str, language: str) -> str:
    """Build the prompt for the interview readiness score.

    Args:
        job_description: The job description text.
        resume_text: Extracted resume text. Callers MUST NOT call this
            with an empty resume; use `not_available_result()` instead.
        language: Display language code ("en", "hi", "te").

    Returns:
        The full prompt string to send to an `LLMClient`.
    """
    return (
        "You are an expert technical recruiter. Based on the job "
        "description and candidate resume below, produce an Interview "
        "Readiness Score.\n\n"
        f"Job description:\n{job_description}\n\n"
        f"Candidate resume:\n{resume_text}\n\n"
        "Respond with ONLY a JSON object (no markdown, no commentary) "
        "with exactly these fields:\n"
        '- "technical_match": integer 0-100\n'
        '- "communication_match": integer 0-100\n'
        '- "domain_match": integer 0-100\n'
        '- "overall_readiness": integer 0-100\n'
        '- "commentary": a short string (2-4 sentences) explaining the '
        "scores and the biggest factors driving them\n\n"
        f"{language_instruction(language)} The JSON field names must "
        'remain in English exactly as given, but the "commentary" VALUE '
        "must be in the requested language.\n"
    )


def _coerce_score(value: object) -> int | None:
    """Coerce a JSON value to an int in [0, 100], or None if invalid."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        score = value
    elif isinstance(value, float):
        score = int(round(value))
    else:
        return None
    if 0 <= score <= 100:
        return score
    return None


def parse_response(raw: str) -> ReadinessScoreResult:
    """Parse the raw LLM response into a `ReadinessScoreResult`.

    Args:
        raw: The raw text response from `LLMClient.generate()`.

    Returns:
        A `ReadinessScoreResult`. If `raw` is not valid JSON in the
        expected shape, or required fields are missing/invalid, returns a
        result with `raw_error` set and `score=None`.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json") :]
        cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return ReadinessScoreResult(
            score=None,
            raw_error="The interview readiness score returned an unexpected format.",
        )

    if not isinstance(data, dict):
        return ReadinessScoreResult(
            score=None,
            raw_error="The interview readiness score returned an unexpected format.",
        )

    technical = _coerce_score(data.get("technical_match"))
    communication = _coerce_score(data.get("communication_match"))
    domain = _coerce_score(data.get("domain_match"))
    overall = _coerce_score(data.get("overall_readiness"))
    commentary = data.get("commentary", "")

    if None in (technical, communication, domain, overall):
        return ReadinessScoreResult(
            score=None,
            raw_error=("The interview readiness score is missing one or more required fields."),
        )

    assert technical is not None
    assert communication is not None
    assert domain is not None
    assert overall is not None

    return ReadinessScoreResult(
        score=ReadinessScore(
            technical_match=technical,
            communication_match=communication,
            domain_match=domain,
            overall_readiness=overall,
            commentary=commentary if isinstance(commentary, str) else "",
        )
    )
