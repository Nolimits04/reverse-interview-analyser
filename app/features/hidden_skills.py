"""Hidden Skills Detector (FR-006).

Produces a table mapping explicit job-description requirements to
inferred "hidden" requirements (soft skills, tooling, collaboration
expectations, etc.).
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.i18n.prompts import language_instruction


@dataclass(frozen=True)
class HiddenSkillRow:
    """A single explicit-requirement -> hidden-requirement mapping."""

    explicit_requirement: str
    hidden_requirement: str


@dataclass(frozen=True)
class HiddenSkillsResult:
    """Result of the hidden skills analysis."""

    rows: list[HiddenSkillRow]
    raw_error: str | None = None

    @property
    def is_fallback(self) -> bool:
        """True if this result is a fallback/error placeholder."""
        return self.raw_error is not None


def build_prompt(job_description: str, company_info: str, language: str) -> str:
    """Build the prompt for hidden-skills inference.

    Args:
        job_description: The job description text.
        company_info: Optional company about/website text (may be empty).
        language: Display language code ("en", "hi", "te").

    Returns:
        The full prompt string to send to an `LLMClient`.
    """
    company_section = f"\nCompany information:\n{company_info}\n" if company_info.strip() else ""

    return (
        "You are an expert technical recruiter. Read the job description "
        "below and identify both the EXPLICIT requirements stated and the "
        "HIDDEN requirements that are implied but not directly stated "
        "(e.g. soft skills, tooling expectations, collaboration norms, "
        "communication or stakeholder-management expectations).\n\n"
        f"Job description:\n{job_description}\n"
        f"{company_section}\n"
        "Respond with ONLY a JSON array (no markdown, no commentary). "
        "Each element must be an object with exactly two string fields: "
        '"explicit_requirement" and "hidden_requirement". Produce between '
        "4 and 10 rows, each pairing one explicit requirement with one "
        "specific inferred hidden requirement.\n\n"
        f"{language_instruction(language)} The JSON field names "
        "(explicit_requirement, hidden_requirement) must remain in "
        "English, but the VALUES must be in the requested language.\n"
    )


def parse_response(raw: str) -> HiddenSkillsResult:
    """Parse the raw LLM response into a `HiddenSkillsResult`.

    Args:
        raw: The raw text response from `LLMClient.generate()`.

    Returns:
        A `HiddenSkillsResult`. If `raw` is not valid JSON in the expected
        shape, returns a result with `raw_error` set and an empty `rows`
        list (per NFR-002, callers should render this as a user-readable
        message rather than crashing).
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
        return HiddenSkillsResult(
            rows=[],
            raw_error="The hidden skills analysis returned an unexpected format.",
        )

    if not isinstance(data, list):
        return HiddenSkillsResult(
            rows=[],
            raw_error="The hidden skills analysis returned an unexpected format.",
        )

    rows: list[HiddenSkillRow] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        explicit = item.get("explicit_requirement")
        hidden = item.get("hidden_requirement")
        if isinstance(explicit, str) and isinstance(hidden, str):
            rows.append(HiddenSkillRow(explicit_requirement=explicit, hidden_requirement=hidden))

    if not rows:
        return HiddenSkillsResult(
            rows=[],
            raw_error="The hidden skills analysis returned no usable rows.",
        )

    return HiddenSkillsResult(rows=rows)
