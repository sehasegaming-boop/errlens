import io
import json
import urllib.error

import pytest

from errlens import ollama_client


def _fake_response(payload: dict):
    class _Resp:
        def __enter__(self_):
            return self_

        def __exit__(self_, *a):
            return False

        def read(self_):
            return json.dumps(payload).encode("utf-8")

    return _Resp()


def test_explain_returns_message(monkeypatch):
    monkeypatch.setattr(
        ollama_client, "_chat_request",
        lambda *a, **k: _fake_response({"message": {"content": " hi "}}),
    )
    assert ollama_client.explain("sys", "user", "m") == "hi"


def test_explain_empty_raises(monkeypatch):
    monkeypatch.setattr(
        ollama_client, "_chat_request",
        lambda *a, **k: _fake_response({"message": {"content": ""}}),
    )
    with pytest.raises(ollama_client.OllamaError):
        ollama_client.explain("sys", "user", "m")


def test_wrap_error_missing_model():
    exc = urllib.error.HTTPError(
        "url", 404, "not found", {}, io.BytesIO(b'{"error":"model not found"}')
    )
    wrapped = ollama_client._wrap_error(exc, "qwen2.5:3b")
    assert "ollama pull qwen2.5:3b" in str(wrapped)


def test_wrap_error_connection():
    exc = urllib.error.URLError("refused")
    wrapped = ollama_client._wrap_error(exc, "m")
    assert "Could not reach Ollama" in str(wrapped)
