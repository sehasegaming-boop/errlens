"""Terminal output helpers: colors and section highlighting."""

import os
import sys

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"

# Colors for the three answer sections.
SECTION_COLORS = {
    "WHAT": "\033[1;36m",        # bold cyan
    "WHY": "\033[1;33m",         # bold yellow
    "HOW TO FIX": "\033[1;32m",  # bold green
}


def supports_color(stream=sys.stdout) -> bool:
    """Decide whether to emit ANSI color codes."""
    if os.environ.get("NO_COLOR"):
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


def colorize_sections(text: str) -> str:
    """Highlight the WHAT / WHY / HOW TO FIX headers in a reply."""
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        for header, color in SECTION_COLORS.items():
            if stripped.upper().startswith(header):
                indent = line[: len(line) - len(stripped)]
                head = stripped[: len(header)]
                rest = stripped[len(header):]
                line = f"{indent}{color}{head}{RESET}{rest}"
                break
        lines.append(line)
    return "\n".join(lines)


def style(text: str, color: str, enabled: bool) -> str:
    """Wrap text in a color code when enabled."""
    return f"{color}{text}{RESET}" if enabled else text
