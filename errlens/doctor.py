"""`errlens doctor` — diagnose the local setup."""

import sys

from . import config, ollama_client, ui


def run() -> int:
    """Check Ollama connectivity and model availability."""
    color = ui.supports_color()
    ok = ui.style("OK", ui.GREEN, color)
    fail = ui.style("FAIL", ui.RED, color)

    print("errlens doctor - checking your setup\n")
    print(f"  Host:           {config.OLLAMA_HOST}")
    print(f"  Default model:  {config.DEFAULT_MODEL}\n")

    if not ollama_client.is_running():
        print(f"  [{fail}] Ollama is not reachable.")
        print("         Start it with:  ollama serve")
        return 1
    print(f"  [{ok}] Ollama is running.")

    try:
        models = ollama_client.list_models()
    except ollama_client.OllamaError as exc:
        print(f"  [{fail}] Could not list models: {exc}")
        return 1

    if not models:
        print(f"  [{fail}] No models installed.")
        print(f"         Pull one with:  ollama pull {config.DEFAULT_MODEL}")
        return 1
    print(f"  [{ok}] {len(models)} model(s) available: {', '.join(models)}")

    # A model tag may be stored as "name:latest"; match on the base name too.
    base = config.DEFAULT_MODEL.split(":")[0]
    has_default = any(
        m == config.DEFAULT_MODEL or m.split(":")[0] == base for m in models
    )
    if has_default:
        print(f"  [{ok}] Default model '{config.DEFAULT_MODEL}' is available.")
    else:
        print(f"  [{fail}] Default model '{config.DEFAULT_MODEL}' is missing.")
        print(f"         Pull it with:  ollama pull {config.DEFAULT_MODEL}")
        return 1

    print("\nAll checks passed. errlens is ready.")
    return 0
