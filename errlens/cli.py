"""Command-line interface for errlens."""

import argparse
import sys

from . import __version__, config
from .ollama_client import OllamaError, explain
from .prompt import SYSTEM_PROMPT, build_prompt

# ANSI color codes for the three sections.
_COLORS = {
    "WHAT": "\033[1;36m",      # bold cyan
    "WHY": "\033[1;33m",       # bold yellow
    "HOW TO FIX": "\033[1;32m",  # bold green
}
_RESET = "\033[0m"
_DIM = "\033[2m"


def _read_error_text(args: argparse.Namespace) -> str:
    """Read the error text from a positional argument or stdin."""
    if args.text:
        return " ".join(args.text)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _colorize(text: str) -> str:
    """Highlight the WHAT / WHY / HOW TO FIX section headers."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        for header, color in _COLORS.items():
            if stripped.upper().startswith(header):
                idx = line.lower().find(header.lower())
                head = line[idx:idx + len(header)]
                rest = line[idx + len(header):]
                line = line[:idx] + color + head + _RESET + rest
                break
        lines.append(line)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="errlens",
        description="Explain a failed terminal command's error locally via Ollama.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Error text to explain. If omitted, read from stdin.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=config.DEFAULT_MODEL,
        help=f"Ollama model to use (default: {config.DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Disable colored output.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"errlens {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    error_text = _read_error_text(args).strip()
    if not error_text:
        print(
            "No error text provided. Pipe a command's output or pass it as an argument:\n"
            "    some_command 2>&1 | errlens\n"
            '    errlens "paste error text here"',
            file=sys.stderr,
        )
        return 2

    prompt = build_prompt(error_text)

    try:
        answer = explain(prompt, SYSTEM_PROMPT, args.model)
    except OllamaError as exc:
        print(f"errlens: {exc}", file=sys.stderr)
        return 1

    use_color = not args.raw and sys.stdout.isatty()
    print(_colorize(answer) if use_color else answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
