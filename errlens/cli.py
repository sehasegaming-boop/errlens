"""Command-line interface for errlens."""

import argparse
import sys

from . import __version__, config, doctor, hooks, ui
from .ollama_client import OllamaError, explain, explain_stream
from .prompt import SYSTEM_PROMPT, build_prompt


def _read_error_text(args: argparse.Namespace) -> str:
    """Read the error text from positional args or stdin."""
    if args.text:
        return " ".join(args.text)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _explain(args: argparse.Namespace) -> int:
    error_text = _read_error_text(args).strip()
    if not error_text:
        print(
            "No error text provided. Pipe a command's output or pass it as an "
            "argument:\n"
            "    some_command 2>&1 | errlens\n"
            '    errlens "paste error text here"\n'
            "    errlens doctor        # check your setup",
            file=sys.stderr,
        )
        return 2

    prompt = build_prompt(error_text)
    color = not args.raw and ui.supports_color()

    try:
        if args.no_stream or not sys.stdout.isatty():
            answer = explain(SYSTEM_PROMPT, prompt, args.model)
            print(ui.colorize_sections(answer) if color else answer)
        else:
            # Stream tokens live for responsiveness on slow CPUs.
            buffer = []
            for chunk in explain_stream(SYSTEM_PROMPT, prompt, args.model):
                buffer.append(chunk)
                sys.stdout.write(chunk)
                sys.stdout.flush()
            sys.stdout.write("\n")
            full = "".join(buffer)
            if color and full.strip():
                # Repaint over the streamed text with colored section headers.
                line_count = full.count("\n") + 1
                sys.stdout.write(f"\033[{line_count}F\033[J")
                sys.stdout.write(ui.colorize_sections(full) + "\n")
    except OllamaError as exc:
        print(f"errlens: {exc}", file=sys.stderr)
        return 1
    return 0


COMMANDS = ("explain", "doctor", "install-hook")


def build_parser() -> argparse.ArgumentParser:
    """Parser for the default 'explain' behavior."""
    parser = argparse.ArgumentParser(
        prog="errlens",
        description="Explain a failed terminal command's error locally via Ollama.",
        epilog="Commands: explain (default), doctor, install-hook [bash|zsh|powershell].",
    )
    parser.add_argument("-V", "--version", action="version",
                        version=f"errlens {__version__}")
    parser.add_argument("text", nargs="*", help="Error text. If omitted, read stdin.")
    parser.add_argument("-m", "--model", default=config.DEFAULT_MODEL,
                        help=f"Ollama model to use (default: {config.DEFAULT_MODEL}).")
    parser.add_argument("--raw", action="store_true", help="Disable colored output.")
    parser.add_argument("--no-stream", action="store_true",
                        help="Wait for the full reply instead of streaming.")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # Dispatch on a leading subcommand; otherwise fall through to 'explain'.
    if argv and argv[0] in COMMANDS:
        command, rest = argv[0], argv[1:]
        if command == "doctor":
            return doctor.run()
        if command == "install-hook":
            shell = rest[0] if rest else None
            return hooks.run(shell)
        argv = rest  # "explain" — parse the remaining args below.

    args = build_parser().parse_args(argv)
    return _explain(args)


if __name__ == "__main__":
    sys.exit(main())
