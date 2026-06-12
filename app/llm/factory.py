"""LLM provider selection.

Per the project constitution (Principle II), the active LLM client is
chosen at runtime in a single, fixed order:

    1. User-supplied Gemini API key (BYOK), if provided.
    2. A locally running Ollama instance, if reachable.
    3. A server-side fallback Gemini API key.

This order MUST be implemented only in `get_llm_client()` below.
"""

from __future__ import annotations

import requests

from app.config import get_settings
from app.llm.client import GeminiClient, LLMClient, OllamaClient


def ollama_is_running(host: str, timeout: float = 1.0) -> bool:
    """Check whether a local Ollama instance is reachable.

    Args:
        host: Base URL of the Ollama instance (e.g. http://localhost:11434).
        timeout: Request timeout in seconds.

    Returns:
        True if Ollama responds successfully to a tags request, False if
        it is unreachable, times out, or returns a non-200 response.
    """
    url = f"{host.rstrip('/')}/api/tags"
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_llm_client(
    user_gemini_key: str | None,
    ollama_host: str | None = None,
    fallback_gemini_key: str | None = None,
) -> LLMClient:
    """Resolve and return the active `LLMClient` for this session.

    Selection order (Principle II):
        1. `user_gemini_key`, if provided -> `GeminiClient`.
        2. A reachable Ollama instance at `ollama_host` -> `OllamaClient`.
        3. `fallback_gemini_key` -> `GeminiClient`.

    Args:
        user_gemini_key: Gemini API key supplied by the user for this
            session, or None/empty if not provided.
        ollama_host: Base URL for a local Ollama instance. Defaults to the
            value from `app.config.get_settings()` if not given.
        fallback_gemini_key: Server-side fallback Gemini API key. Defaults
            to the value from `app.config.get_settings()` if not given.

    Returns:
        An `LLMClient` instance ready to use.

    Raises:
        RuntimeError: If no provider can be resolved (no user key, Ollama
            unreachable, and no usable fallback key).
    """
    settings = get_settings()
    resolved_ollama_host = ollama_host or settings.ollama_host
    resolved_fallback_key = fallback_gemini_key or settings.fallback_gemini_api_key

    if user_gemini_key:
        return GeminiClient(api_key=user_gemini_key, model=settings.gemini_model)

    if ollama_is_running(resolved_ollama_host):
        return OllamaClient(host=resolved_ollama_host, model=settings.ollama_model)

    if resolved_fallback_key:
        return GeminiClient(api_key=resolved_fallback_key, model=settings.gemini_model)

    raise RuntimeError(
        "No LLM provider available: no API key was provided, no local "
        "Ollama instance is reachable, and no fallback API key is "
        "configured on the server."
    )
