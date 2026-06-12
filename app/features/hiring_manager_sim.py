"""Hiring Manager Simulation (FR-011).

Produces a short narrative describing likely concerns a hiring manager
would have about this candidate for this role.

Unlike the other feature modules, this produces free-form narrative text
rather than structured JSON, so `parse_response` mainly validates that a
non-empty response was returned.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.i18n.prompts import language_instruction


@dataclass(frozen=True)
class HiringManagerSimResult:
    """Result of the hiring manager simulation."""

    narrative: str
    raw_error: str | None = None

    @property
    def is_fallback(self) -> bool:
        """True if this result is a fallback/error placeholder."""
        return self.raw_error is not None


def build_prompt(
    job_description: str,
    company_info: str,
    resume_text: str,
    language: str,
) -> str:
    """Build the prompt for the hiring manager simulation.

    Args:
        job_description: The job description text.
        company_info: Optional company about/website text (may be empty).
        resume_text: Extracted resume text, or an empty string if no
            resume was provided.
        language: Display language code ("en", "hi", "te").

    Returns:
        The full prompt string to send to an `LLMClient`.
    """
    company_section = f"\nCompany information:\n{company_info}\n" if company_info.strip() else ""
    resume_section = (
        f"\nCandidate resume:\n{resume_text}\n"
        if resume_text.strip()
        else "\nNo resume was provided; comment on likely concerns based "
        "on the job description and company information alone, and note "
        "that a resume was not available for a fuller assessment.\n"
    )

    return (
        "Pretend you are the hiring manager for the role described "
        "below. Write a short, candid narrative (3-6 sentences) "
        "describing the concerns or open questions you would have about "
        "this candidate for this role. Be specific and constructive, not "
        "generic — reference particular aspects of the job description, "
        "company context, and (if provided) the resume.\n\n"
        f"Job description:\n{job_description}\n"
        f"{company_section}"
        f"{resume_section}\n"
        "Respond with plain text only (no markdown headers, no JSON, no "
        "preamble like 'As the hiring manager,'). Just the narrative "
        "itself.\n\n"
        f"{language_instruction(language)}\n"
    )


def parse_response(raw: str) -> HiringManagerSimResult:
    """Parse the raw LLM response into a `HiringManagerSimResult`.

    Args:
        raw: The raw text response from `LLMClient.generate()`.

    Returns:
        A `HiringManagerSimResult`. If `raw` is empty or whitespace-only,
        returns a result with `raw_error` set.
    """
    cleaned = raw.strip()
    if not cleaned:
        return HiringManagerSimResult(
            narrative="",
            raw_error="The hiring manager simulation returned an empty response.",
        )
    return HiringManagerSimResult(narrative=cleaned)
