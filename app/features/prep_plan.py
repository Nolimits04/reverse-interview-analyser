"""Prioritized Preparation Plan (FR-010).

Produces recommended preparation topics grouped into priority tiers
(e.g. Priority 1, Priority 2, Priority 3) rather than a flat list.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.i18n.prompts import language_instruction


@dataclass(frozen=True)
class PriorityTier:
    """A priority tier and its recommended preparation topics."""

    priority_label: str
    topics: list[str]


@dataclass(frozen=True)
class PrepPlanResult:
    """Result of the preparation plan generation."""

    tiers: list[PriorityTier]
    raw_error: str | None = None

    @property
    def is_fallback(self) -> bool:
        """True if this result is a fallback/error placeholder."""
        return self.raw_error is not None


def build_prompt(
    job_description: str,
    resume_text: str,
    language: str,
) -> str:
    """Build the prompt for the prioritized preparation plan.

    Args:
        job_description: The job description text.
        resume_text: Extracted resume text, or an empty string if no
            resume was provided. If empty, the plan should focus on the
            job description's requirements generally.
        language: Display language code ("en", "hi", "te").

    Returns:
        The full prompt string to send to an `LLMClient`.
    """
    resume_section = (
        f"\nCandidate resume:\n{resume_text}\n"
        if resume_text.strip()
        else "\nNo resume was provided; base the plan on the job "
        "description's requirements generally.\n"
    )

    return (
        "You are a career coach. Based on the job description below "
        "(and resume, if provided), create a prioritized interview "
        "preparation plan.\n\n"
        f"Job description:\n{job_description}\n"
        f"{resume_section}\n"
        "Group preparation topics into priority tiers, where Priority 1 "
        "topics are the most urgent/important to prepare and later "
        "priorities are progressively less urgent. Produce 2 to 4 tiers, "
        "each with 2 to 6 specific, actionable topics (not vague advice "
        'like "learn Docker" — instead specify what aspect, e.g. '
        '"Docker: container lifecycle, image layers, Dockerfile '
        'best practices").\n\n'
        "Respond with ONLY a JSON array (no markdown, no commentary). "
        'Each element must be an object with fields: "priority_label" '
        '(string, e.g. "Priority 1") and "topics" (array of strings).\n\n'
        f"{language_instruction(language)} The JSON field names "
        "(priority_label, topics) must remain in English, but the "
        "VALUES must be in the requested language (including the "
        'priority label text itself, e.g. translate "Priority 1" '
        "appropriately).\n"
    )


def parse_response(raw: str) -> PrepPlanResult:
    """Parse the raw LLM response into a `PrepPlanResult`.

    Args:
        raw: The raw text response from `LLMClient.generate()`.

    Returns:
        A `PrepPlanResult`. If `raw` is not valid JSON in the expected
        shape, returns a result with `raw_error` set and an empty `tiers`
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
        return PrepPlanResult(
            tiers=[],
            raw_error="The preparation plan returned an unexpected format.",
        )

    if not isinstance(data, list):
        return PrepPlanResult(
            tiers=[],
            raw_error="The preparation plan returned an unexpected format.",
        )

    tiers: list[PriorityTier] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        label = item.get("priority_label")
        topics = item.get("topics")
        if isinstance(label, str) and isinstance(topics, list):
            valid_topics = [topic for topic in topics if isinstance(topic, str)]
            if valid_topics:
                tiers.append(PriorityTier(priority_label=label, topics=valid_topics))

    if not tiers:
        return PrepPlanResult(
            tiers=[],
            raw_error="The preparation plan returned no usable tiers.",
        )

    return PrepPlanResult(tiers=tiers)
