"""Minimal Ollama client built on the standard library only."""

import json
import urllib.error
import urllib.request

from . import config


class OllamaError(Exception):
    """Raised when the local Ollama server cannot fulfill a request."""


def explain(error_text: str, system_prompt: str, model: str) -> str:
    """Send the prompt to the local Ollama model and return the reply.

    Uses the /api/chat endpoint with streaming disabled for simplicity.
    """
    url = f"{config.OLLAMA_HOST}/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": error_text},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(request, timeout=config.TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        if exc.code == 404 and "model" in detail.lower():
            raise OllamaError(
                f"Model '{model}' not found. Pull it first:\n"
                f"    ollama pull {model}"
            ) from exc
        raise OllamaError(
            f"Ollama returned HTTP {exc.code}: {detail.strip()}"
        ) from exc
    except urllib.error.URLError as exc:
        raise OllamaError(
            f"Could not reach Ollama at {config.OLLAMA_HOST}. "
            "Is it running? Try:\n    ollama serve"
        ) from exc

    message = body.get("message", {}).get("content", "").strip()
    if not message:
        raise OllamaError("Ollama returned an empty response.")
    return message
