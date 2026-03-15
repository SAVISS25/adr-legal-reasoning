"""Tests for adr_legal_reasoning.extractor."""

from unittest.mock import MagicMock, patch

import pytest

from adr_legal_reasoning.extractor import extract_theoretical_dna


SAMPLE_PAPER = "Full text of a legal paper about mediation theory."
SAMPLE_ANALYSIS = "PAPER METADATA\n- Full citation: Author, Title, Journal, 2023"


def _make_mock_client(content: str = SAMPLE_ANALYSIS):
    """Return a mock openai.OpenAI client that returns ``content``."""
    mock_message = MagicMock()
    mock_message.content = content

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


class TestExtractTheoreticalDna:
    @patch("adr_legal_reasoning.extractor.openai")
    def test_returns_string(self, mock_openai):
        mock_openai.OpenAI.return_value = _make_mock_client()
        result = extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-test")
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("adr_legal_reasoning.extractor.openai")
    def test_returns_model_content(self, mock_openai):
        mock_openai.OpenAI.return_value = _make_mock_client(SAMPLE_ANALYSIS)
        result = extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-test")
        assert result == SAMPLE_ANALYSIS

    @patch("adr_legal_reasoning.extractor.openai")
    def test_passes_system_prompt(self, mock_openai):
        from adr_legal_reasoning.prompts import SYSTEM_PROMPT
        mock_client = _make_mock_client()
        mock_openai.OpenAI.return_value = mock_client
        extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-test")
        call_kwargs = mock_client.chat.completions.create.call_args
        messages = call_kwargs.kwargs.get("messages") or call_kwargs.args[0] if call_kwargs.args else []
        if not messages:
            messages = call_kwargs[1].get("messages", [])
        system_messages = [m for m in messages if m.get("role") == "system"]
        assert system_messages, "No system message was sent"
        assert system_messages[0]["content"] == SYSTEM_PROMPT

    @patch("adr_legal_reasoning.extractor.openai")
    def test_passes_paper_text_in_user_message(self, mock_openai):
        mock_client = _make_mock_client()
        mock_openai.OpenAI.return_value = mock_client
        extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-test")
        call_kwargs = mock_client.chat.completions.create.call_args
        messages = call_kwargs[1].get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]
        assert user_messages, "No user message was sent"
        assert SAMPLE_PAPER in user_messages[0]["content"]

    @patch("adr_legal_reasoning.extractor.openai")
    def test_uses_default_model(self, mock_openai):
        mock_client = _make_mock_client()
        mock_openai.OpenAI.return_value = mock_client
        extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-test")
        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs[1].get("model") == "gpt-4o"

    @patch("adr_legal_reasoning.extractor.openai")
    def test_uses_custom_model(self, mock_openai):
        mock_client = _make_mock_client()
        mock_openai.OpenAI.return_value = mock_client
        extract_theoretical_dna(SAMPLE_PAPER, model="gpt-4-turbo", api_key="sk-test")
        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs[1].get("model") == "gpt-4-turbo"

    @patch("adr_legal_reasoning.extractor.openai")
    def test_passes_api_key_to_client(self, mock_openai):
        mock_openai.OpenAI.return_value = _make_mock_client()
        extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-explicit")
        mock_openai.OpenAI.assert_called_once()
        init_kwargs = mock_openai.OpenAI.call_args[1]
        assert init_kwargs.get("api_key") == "sk-explicit"

    @patch("adr_legal_reasoning.extractor.openai")
    def test_passes_base_url_to_client(self, mock_openai):
        mock_openai.OpenAI.return_value = _make_mock_client()
        extract_theoretical_dna(SAMPLE_PAPER, api_key="sk-test", base_url="http://localhost")
        init_kwargs = mock_openai.OpenAI.call_args[1]
        assert init_kwargs.get("base_url") == "http://localhost"

    @patch("adr_legal_reasoning.extractor.openai")
    def test_empty_paper_raises_value_error(self, mock_openai):
        mock_openai.OpenAI.return_value = _make_mock_client()
        with pytest.raises(ValueError):
            extract_theoretical_dna("", api_key="sk-test")

    @patch("adr_legal_reasoning.extractor.openai")
    def test_whitespace_paper_raises_value_error(self, mock_openai):
        mock_openai.OpenAI.return_value = _make_mock_client()
        with pytest.raises(ValueError):
            extract_theoretical_dna("   \n\t  ", api_key="sk-test")

    @patch("adr_legal_reasoning.extractor.openai")
    def test_env_var_api_key_used_when_no_explicit_key(self, mock_openai, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-from-env")
        mock_openai.OpenAI.return_value = _make_mock_client()
        extract_theoretical_dna(SAMPLE_PAPER)
        init_kwargs = mock_openai.OpenAI.call_args[1]
        assert init_kwargs.get("api_key") == "sk-from-env"
