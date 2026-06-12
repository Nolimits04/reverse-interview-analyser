"""LLM provider abstraction.

Per the project constitution (Principle I), all AI interactions MUST go
through the `LLMClient` interface. Feature modules call
`get_llm_client().generate(prompt)` and MUST NOT call any provider SDK or
HTTP API directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import requests


class LLMClient(ABC):
    """Common interface for all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs: object) -> str:
        """Generate a text completion for the given prompt.

        Args:
            prompt: The full prompt text to send to the model.
            **kwargs: Provider-specific generation options (e.g.
                temperature). Implementations should ignore options they
                do not support.

        Returns:
            The raw text response from the model.

        Raises:
            RuntimeError: If the provider request fails.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """A short, user-facing name for this provider (for UI display)."""
        raise NotImplementedError


class GeminiClient(LLMClient):
    """LLM client backed by the Google Gemini API."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        if not api_key:
            raise ValueError("GeminiClient requires a non-empty api_key")
        self._api_key = api_key
        self._model = model

    @property
    def provider_name(self) -> str:
        return f"Gemini ({self._model})"

    def generate(self, prompt: str, **kwargs: object) -> str:
        try:
            import google.generativeai as genai
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError(
                "google-generativeai package is not installed"
            ) from exc

        try:
            genai.configure(api_key=self._api_key)
            model = genai.GenerativeModel(self._model)
            response = model.generate_content(prompt)
            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned an empty response")
            return text
        except Exception as exc:
            raise RuntimeError(f"Gemini request failed: {exc}") from exc


class OllamaClient(LLMClient):
    """LLM client backed by a local Ollama instance."""

    def __init__(self, host: str, model: str = "llama3", timeout: float = 60.0) -> None:
        if not host:
            raise ValueError("OllamaClient requires a non-empty host")
        self._host = host.rstrip("/")
        self._model = model
        self._timeout = timeout

    @property
    def provider_name(self) -> str:
        return f"Ollama ({self._model}, local)"

    def generate(self, prompt: str, **kwargs: object) -> str:
        url = f"{self._host}/api/generate"
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            response = requests.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc

        text = data.get("response")
        if not text:
            raise RuntimeError("Ollama returned an empty response")
        return text
