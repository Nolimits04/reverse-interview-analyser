"""Language-instruction helpers for LLM prompts (Principle III).

Each feature module's prompt should end with a language instruction
generated here, so that AI-generated content is produced in the user's
selected display language (English, Hindi, or Telugu).
"""

from __future__ import annotations

SUPPORTED_LANGUAGES = {"en", "hi", "te"}

_LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
}


def language_instruction(language: str) -> str:
    """Return an instruction string to append to a prompt.

    Args:
        language: A language code: "en", "hi", or "te".

    Returns:
        An instruction sentence telling the model which language to
        respond in. For English, this is still explicit (rather than
        empty) so prompt structure stays consistent across languages.

    Raises:
        ValueError: If `language` is not one of the supported codes.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language code: {language!r}. "
            f"Supported codes: {sorted(SUPPORTED_LANGUAGES)}"
        )

    name = _LANGUAGE_NAMES[language]
    return (
        f"Respond entirely in {name}. Do not include any text in other "
        f"languages, including headings and labels within the response."
    )


def language_name(language: str) -> str:
    """Return the human-readable name for a language code.

    Raises:
        ValueError: If `language` is not one of the supported codes.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language code: {language!r}. "
            f"Supported codes: {sorted(SUPPORTED_LANGUAGES)}"
        )
    return _LANGUAGE_NAMES[language]
