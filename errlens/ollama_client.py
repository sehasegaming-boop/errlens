"""Minimal Ollama client built on the standard library only."""

import json
import urllib.error
import urllib.request
from collections.abc import Iterator

from . import config


class OllamaError(Exception):
    """Raised when the local Ollama server cannot fulfill a request."""


def _chat_request(system_prompt: str, user_prompt: str, model: str, stream: bool):
    """Build and open a request against the Ollama /api/chat endpoint."""
    url = f"{config.OLLAMA_HOST}/api/chat"
    payload = {
        "model": model,
        "stream": stream,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    return urllib.request.urlopen(request, timeout=config.TIMEOUT)


def _wrap_error(exc: Exception, model: str) -> OllamaError:
    """Translate low-level network errors into actionable messages."""
    if isinstance(exc, urllib.error.HTTPError):
        detail = exc.read().decode("utf-8", "replace")
        if exc.code == 404 and "model" in detail.lower():
            return OllamaError(
                f"Model '{model}' not found. Pull it first:\n"
                f"    ollama pull {model}"
            )
        return OllamaError(f"Ollama returned HTTP {exc.code}: {detail.strip()}")
    if isinstance(exc, urllib.error.URLError):
        return OllamaError(
            f"Could not reach Ollama at {config.OLLAMA_HOST}. "
            "Is it running? Try:\n    ollama serve"
        )
    return OllamaError(str(exc))


def explain(system_prompt: str, user_prompt: str, model: str) -> str:
    """Send the prompt to the local model and return the full reply."""
    try:
        with _chat_request(system_prompt, user_prompt, model, stream=False) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise _wrap_error(exc, model) from exc

    message = body.get("message", {}).get("content", "").strip()
    if not message:
        raise OllamaError("Ollama returned an empty response.")
    return message


def explain_stream(system_prompt: str, user_prompt: str, model: str) -> Iterator[str]:
    """Stream the model reply, yielding content chunks as they arrive."""
    try:
        resp = _chat_request(system_prompt, user_prompt, model, stream=True)
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise _wrap_error(exc, model) from exc

    with resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            chunk = json.loads(line)
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
            if chunk.get("done"):
                break


def is_running() -> bool:
    """Return True if the local Ollama server responds."""
    try:
        with urllib.request.urlopen(f"{config.OLLAMA_HOST}/api/tags", timeout=5):
            return True
    except (urllib.error.URLError, OSError):
        return False


def list_models() -> list[str]:
    """Return the names of locally available models."""
    try:
        with urllib.request.urlopen(f"{config.OLLAMA_HOST}/api/tags", timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError) as exc:
        raise _wrap_error(exc, "") from exc
    return [m.get("name", "") for m in body.get("models", [])]
