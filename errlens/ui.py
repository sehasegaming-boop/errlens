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


def _enable_windows_vt() -> bool:
    """Enable ANSI escape processing on the Windows console.

    Modern Windows consoles support virtual terminal sequences but do not
    always enable them by default. Returns True if escape codes will render.
    """
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        enable_vt = 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        if mode.value & enable_vt:
            return True
        return bool(kernel32.SetConsoleMode(handle, mode.value | enable_vt))
    except Exception:
        return False


def supports_color(stream=sys.stdout) -> bool:
    """Decide whether to emit ANSI color codes."""
    if os.environ.get("NO_COLOR"):
        return False
    if not bool(getattr(stream, "isatty", lambda: False)()):
        return False
    # On Windows, only emit color if VT processing can be turned on; otherwise
    # the raw escape codes would be printed as garbage.
    return _enable_windows_vt()


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
