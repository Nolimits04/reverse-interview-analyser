"""Environment configuration loading for InterviewIQ.

All configuration is read from environment variables (optionally loaded
from a local .env file via python-dotenv). No secrets are hard-coded or
written to disk by this module.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is an optional convenience
    pass


@dataclass(frozen=True)
class Settings:
    """Resolved application settings sourced from the environment."""

    fallback_gemini_api_key: str | None
    ollama_host: str
    ollama_model: str
    gemini_model: str


def get_settings() -> Settings:
    """Load and return application settings from environment variables.

    Environment variables:
        FALLBACK_GEMINI_API_KEY: Server-side Gemini key used only when the
            user has not supplied their own key and Ollama is unreachable.
        OLLAMA_HOST: Base URL for a local Ollama instance
            (default: http://localhost:11434).
        OLLAMA_MODEL: Model name to use with Ollama (default: llama3).
        GEMINI_MODEL: Gemini model name (default: gemini-2.5-flash).
    """
    return Settings(
        fallback_gemini_api_key=os.environ.get("FALLBACK_GEMINI_API_KEY") or None,
        ollama_host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        ollama_model=os.environ.get("OLLAMA_MODEL", "llama3"),
        gemini_model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    )
