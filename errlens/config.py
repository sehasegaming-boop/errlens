"""Configuration and defaults for errlens.

Values can be overridden via environment variables so users do not have to
pass flags every time.
"""

import os

# Default local Ollama model. Small enough to run on CPU.
DEFAULT_MODEL = os.environ.get("ERRLENS_MODEL", "qwen2.5:3b")

# Ollama HTTP endpoint. Local by default; data never leaves the machine.
OLLAMA_HOST = os.environ.get("ERRLENS_HOST", "http://localhost:11434")

# Request timeout in seconds. CPU inference can be slow on first token.
TIMEOUT = int(os.environ.get("ERRLENS_TIMEOUT", "120"))
