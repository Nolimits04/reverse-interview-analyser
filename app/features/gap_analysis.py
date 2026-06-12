"""Resume Gap Analysis (FR-008).

Compares the resume against the job description, categorizing
skills/requirements as Strong Match, Weak Match, or Missing.

Per the spec edge case, if no resume is provided, this module returns a
sentinel "not available" result rather than calling the LLM.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.i18n.prompts import language_instruction

NOT_AVAILABLE_REASON = "No resume was provided, so a resume gap analysis is not available."


@dataclass(frozen=True)
class GapAnalysisItem:
    """A single skill/requirement and its match category."""

    requirement: str
    category: str  # "strong_match" | "weak_match" | "missing"
    note: str = ""


@dataclass(frozen=True)
class GapAnalysisResult:
    """Result of the resume gap analysis."""

    items: list[GapAnalysisItem]
    raw_error: str | None = None
    not_available_reason: str | None = None

    @property
    def is_fallback(self) -> bool:
        """True if this result is a fallback/error placeholder."""
        return self.raw_error is not None

    @property
    def is_available(self) -> bool:
        """True if a gap analysis was actually produced."""
        return self.not_available_reason is None and self.raw_error is None


def not_available_result() -> GapAnalysisResult:
    """Return the sentinel result used when no resume was provided."""
    return GapAnalysisResult(items=[], not_available_reason=NOT_AVAILABLE_REASON)


def build_prompt(job_description: str, resume_text: str, language: str) -> str:
    """Build the prompt for resume gap analysis.

    Args:
        job_description: The job description text.
        resume_text: Extracted resume text. Callers MUST NOT call this
            with an empty resume; use `not_available_result()` instead.
        language: Display language code ("en", "hi", "te").

    Returns:
        The full prompt string to send to an `LLMClient`.
    """
    return (
        "You are an expert technical recruiter. Compare the candidate's "
        "resume against the job description below. For each significant "
        "skill or requirement in the job description, categorize the "
        'candidate\'s match as one of: "strong_match", "weak_match", or '
        '"missing".\n\n'
        f"Job description:\n{job_description}\n\n"
        f"Candidate resume:\n{resume_text}\n\n"
        "Produce between 5 and 12 items covering the most important "
        "requirements. Respond with ONLY a JSON array (no markdown, no "
        "commentary). Each element must be an object with fields: "
        '"requirement" (string), "category" (one of "strong_match", '
        '"weak_match", "missing"), and "note" (short string explaining '
        "the assessment, may be empty).\n\n"
        f"{language_instruction(language)} The JSON field names "
        '(requirement, category, note) and the "category" values '
        "(strong_match, weak_match, missing) must remain in English "
        'exactly as given, but the "requirement" and "note" VALUES must '
        "be in the requested language.\n"
    )


_VALID_CATEGORIES = {"strong_match", "weak_match", "missing"}


def parse_response(raw: str) -> GapAnalysisResult:
    """Parse the raw LLM response into a `GapAnalysisResult`.

    Args:
        raw: The raw text response from `LLMClient.generate()`.

    Returns:
        A `GapAnalysisResult`. If `raw` is not valid JSON in the expected
        shape, returns a result with `raw_error` set and an empty `items`
        list.
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
        return GapAnalysisResult(
            items=[],
            raw_error="The resume gap analysis returned an unexpected format.",
        )

    if not isinstance(data, list):
        return GapAnalysisResult(
            items=[],
            raw_error="The resume gap analysis returned an unexpected format.",
        )

    items: list[GapAnalysisItem] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        requirement = item.get("requirement")
        category = item.get("category")
        note = item.get("note", "")
        if (
            isinstance(requirement, str)
            and isinstance(category, str)
            and category in _VALID_CATEGORIES
        ):
            items.append(
                GapAnalysisItem(
                    requirement=requirement,
                    category=category,
                    note=note if isinstance(note, str) else "",
                )
            )

    if not items:
        return GapAnalysisResult(
            items=[],
            raw_error="The resume gap analysis returned no usable items.",
        )

    return GapAnalysisResult(items=items)
