# errlens

**A local-first terminal error explainer.** When a command fails, errlens reads
the error output and tells you **what** the error is, **why** it happened, and
**how to fix it** — all powered by a local [Ollama](https://ollama.com) model.

> 🔒 **Privacy first.** Your error output never leaves your machine. errlens
> talks only to a local Ollama server. No cloud, no telemetry.

## How it works

```
command fails  →  capture stderr  →  local Ollama model  →  What / Why / How to fix
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- A pulled model (default: `qwen2.5:3b`, comfortable on CPU)

```bash
ollama pull qwen2.5:3b
```

> No GPU needed. On CPU the first response may take a few seconds.

## Install

```bash
pip install .
```

This installs the `errlens` command.

## Usage

Pipe a failing command's output:

```bash
some_command 2>&1 | errlens
```

Or pass the error text directly:

```bash
errlens "ModuleNotFoundError: No module named 'requests'"
```

### Options

| Flag | Description |
| --- | --- |
| `-m`, `--model` | Ollama model to use (default: `qwen2.5:3b`). |
| `--raw` | Disable colored output. |
| `-V`, `--version` | Show version. |

### Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `ERRLENS_MODEL` | `qwen2.5:3b` | Default model. |
| `ERRLENS_HOST` | `http://localhost:11434` | Ollama endpoint. |
| `ERRLENS_TIMEOUT` | `120` | Request timeout (seconds). |

## Roadmap

- Automatic shell-hook capture of the last failed command
- Optional cloud backend (Gemini) — local stays the default
- Error history / caching

## License

MIT
