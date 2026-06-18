# errlens

[![CI](https://github.com/yourname/errlens/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/errlens/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A local-first terminal error explainer.** When a command fails, errlens reads
the error output and tells you **what** the error is, **why** it happened, and
**how to fix it** — all powered by a local [Ollama](https://ollama.com) model.

> 🔒 **Privacy first.** Your error output never leaves your machine. errlens
> talks only to a local Ollama server. No cloud, no telemetry.

> ⚡ **Zero dependencies.** Pure Python standard library. Responses stream
> token-by-token so you are not left staring at a blank screen on CPU.

<!-- Record with: see docs/demo.md -->
![errlens demo](docs/demo.gif)

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

This installs the `errlens` command. Verify your setup any time with:

```bash
errlens doctor
```

## Usage

Pipe a failing command's output:

```bash
some_command 2>&1 | errlens
```

Or pass the error text directly:

```bash
errlens "ModuleNotFoundError: No module named 'requests'"
```

### Shell integration (the fast path)

Install the `err` shortcut so you can explain the last failed command without
retyping anything:

```bash
errlens install-hook          # auto-detects your shell
errlens install-hook zsh      # or name it explicitly
```

Add the printed snippet to your shell profile. Then, whenever a command fails:

```bash
$ npm run build      # fails
$ err                # re-runs it and explains the error
```

Supported shells: **bash**, **zsh**, **PowerShell**.

### Commands

| Command | Description |
| --- | --- |
| `errlens [text]` | Explain piped or argument error text (default). |
| `errlens doctor` | Check Ollama connectivity and model availability. |
| `errlens install-hook [shell]` | Print the `err` shell integration snippet. |

### Options

| Flag | Description |
| --- | --- |
| `-m`, `--model` | Ollama model to use (default: `qwen2.5:3b`). |
| `--raw` | Disable colored output. |
| `--no-stream` | Wait for the full reply instead of streaming. |
| `-V`, `--version` | Show version. |

### Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `ERRLENS_MODEL` | `qwen2.5:3b` | Default model. |
| `ERRLENS_HOST` | `http://localhost:11434` | Ollama endpoint. |
| `ERRLENS_TIMEOUT` | `120` | Request timeout (seconds). |

## Development

```bash
pip install -e ".[dev]"
pytest -q
```

Tests mock the network, so Ollama is not required to run them.

## Roadmap

- Automatic shell-hook capture of the last failed command
- Optional cloud backend (Gemini) — local stays the default
- Error history / caching

## License

MIT
