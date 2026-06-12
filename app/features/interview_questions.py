"""Likely Interview Questions (FR-007).

Produces a list of likely interview questions tailored to the specific
job description and company information, grouped by topic/category.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.i18n.prompts import language_instruction


@dataclass(frozen=True)
class QuestionGroup:
    """A topic/category and its associated interview questions."""

    topic: str
    questions: list[str]


@dataclass(frozen=True)
class InterviewQuestionsResult:
    """Result of the interview questions generation."""

    groups: list[QuestionGroup]
    raw_error: str | None = None

    @property
    def is_fallback(self) -> bool:
        """True if this result is a fallback/error placeholder."""
        return self.raw_error is not None


def build_prompt(job_description: str, company_info: str, language: str) -> str:
    """Build the prompt for likely interview questions.

    Args:
        job_description: The job description text.
        company_info: Optional company about/website text (may be empty).
        language: Display language code ("en", "hi", "te").

    Returns:
        The full prompt string to send to an `LLMClient`.
    """
    company_section = f"\nCompany information:\n{company_info}\n" if company_info.strip() else ""

    return (
        "You are a hiring manager preparing interview questions for the "
        "role described below. Generate likely interview questions that "
        "are SPECIFIC to this job description and company (avoid generic "
        "boilerplate questions that could apply to any role).\n\n"
        f"Job description:\n{job_description}\n"
        f"{company_section}\n"
        "Group the questions by topic/category (e.g. 'Technical Skills', "
        "'System Design', 'Behavioral', 'Domain Knowledge', "
        "'Communication & Collaboration'). Produce 3 to 6 topic groups, "
        "each with 2 to 5 questions.\n\n"
        "Respond with ONLY a JSON array (no markdown, no commentary). "
        'Each element must be an object with two fields: "topic" '
        '(string) and "questions" (array of strings).\n\n'
        f"{language_instruction(language)} The JSON field names (topic, "
        "questions) must remain in English, but the VALUES must be in "
        "the requested language.\n"
    )


def parse_response(raw: str) -> InterviewQuestionsResult:
    """Parse the raw LLM response into an `InterviewQuestionsResult`.

    Args:
        raw: The raw text response from `LLMClient.generate()`.

    Returns:
        An `InterviewQuestionsResult`. If `raw` is not valid JSON in the
        expected shape, returns a result with `raw_error` set and an empty
        `groups` list.
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
        return InterviewQuestionsResult(
            groups=[],
            raw_error="The interview questions generation returned an unexpected format.",
        )

    if not isinstance(data, list):
        return InterviewQuestionsResult(
            groups=[],
            raw_error="The interview questions generation returned an unexpected format.",
        )

    groups: list[QuestionGroup] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        topic = item.get("topic")
        questions = item.get("questions")
        if isinstance(topic, str) and isinstance(questions, list):
            valid_questions = [q for q in questions if isinstance(q, str)]
            if valid_questions:
                groups.append(QuestionGroup(topic=topic, questions=valid_questions))

    if not groups:
        return InterviewQuestionsResult(
            groups=[],
            raw_error="The interview questions generation returned no usable groups.",
        )

    return InterviewQuestionsResult(groups=groups)
