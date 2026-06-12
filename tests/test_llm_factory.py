"""Tests for app.llm.factory: provider selection order (Principle II)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from app.llm.client import GeminiClient, OllamaClient
from app.llm.factory import get_llm_client, ollama_is_running


class _FakeResponse:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


def test_ollama_is_running_true_on_200() -> None:
    with patch("app.llm.factory.requests.get", return_value=_FakeResponse(200)):
        assert ollama_is_running("http://localhost:11434") is True


def test_ollama_is_running_false_on_non_200() -> None:
    with patch("app.llm.factory.requests.get", return_value=_FakeResponse(500)):
        assert ollama_is_running("http://localhost:11434") is False


def test_ollama_is_running_false_on_connection_error() -> None:
    import requests

    with patch(
        "app.llm.factory.requests.get",
        side_effect=requests.ConnectionError("refused"),
    ):
        assert ollama_is_running("http://localhost:11434") is False


def test_user_api_key_takes_priority() -> None:
    """A user-supplied Gemini key wins regardless of Ollama availability."""
    with patch("app.llm.factory.ollama_is_running", return_value=True):
        client = get_llm_client(user_gemini_key="user-key-123")

    assert isinstance(client, GeminiClient)
    assert "Gemini" in client.provider_name


def test_falls_back_to_ollama_when_no_user_key_and_ollama_running() -> None:
    with patch("app.llm.factory.ollama_is_running", return_value=True):
        client = get_llm_client(user_gemini_key=None, ollama_host="http://localhost:11434")

    assert isinstance(client, OllamaClient)
    assert "Ollama" in client.provider_name


def test_falls_back_to_server_gemini_key_when_no_user_key_and_no_ollama() -> None:
    with patch("app.llm.factory.ollama_is_running", return_value=False):
        client = get_llm_client(
            user_gemini_key=None,
            ollama_host="http://localhost:11434",
            fallback_gemini_key="server-key-456",
        )

    assert isinstance(client, GeminiClient)
    assert "Gemini" in client.provider_name


def test_raises_when_no_provider_available() -> None:
    with patch("app.llm.factory.ollama_is_running", return_value=False):
        with pytest.raises(RuntimeError):
            get_llm_client(
                user_gemini_key=None,
                ollama_host="http://localhost:11434",
                fallback_gemini_key=None,
            )


def test_empty_string_user_key_is_treated_as_absent() -> None:
    """An empty string key should not be passed to GeminiClient (Principle II)."""
    with patch("app.llm.factory.ollama_is_running", return_value=True):
        client = get_llm_client(user_gemini_key="")

    assert isinstance(client, OllamaClient)
