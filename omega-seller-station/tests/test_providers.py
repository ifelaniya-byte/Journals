import pytest

from omega.config import Config
from omega.providers import MockProvider, OpenAICompatibleProvider, create_provider


def test_mock_needs_no_network():
    text = MockProvider().generate("hello")["text"]
    assert "requested_verdict" in text


def test_live_provider_fail_closed_without_network():
    cfg = Config(model_provider="openai-compatible", allow_network=False)
    with pytest.raises(RuntimeError, match="allow_network is false"):
        create_provider(cfg)


def test_live_provider_fail_closed_without_key():
    cfg = Config(
        model_provider="openai-compatible",
        allow_network=True,
        api_key_env="OMEGA_MISSING_KEY",
    )
    with pytest.raises(RuntimeError, match="fail-closed"):
        create_provider(cfg)


def test_http_non_loopback_rejected():
    with pytest.raises(RuntimeError, match="non-loopback HTTP"):
        OpenAICompatibleProvider("k", "http://example.com/v1", "x")


def test_loopback_http_allowed_for_ollama():
    OpenAICompatibleProvider("", "http://127.0.0.1:11434/v1", "llama")
