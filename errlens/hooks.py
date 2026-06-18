"""`errlens install-hook` — shell integration snippets.

Defines an `err` shortcut that re-runs your previous command, captures its
output, and pipes it to errlens. This is the fastest way to explain a failure:
run a command, watch it fail, then just type `err`.
"""

import sys

_BASH_ZSH = r"""
# >>> errlens shell integration >>>
# Re-run the previous command, capture its output, and explain it.
err() {
  local last
  last=$(fc -ln -1)
  printf '\033[2m$ %s\033[0m\n' "$last"
  eval "$last" 2>&1 | errlens
}
# <<< errlens shell integration <<<
""".strip()

_POWERSHELL = r"""
# >>> errlens shell integration >>>
# Re-run the previous command, capture its output, and explain it.
function err {
  $last = (Get-History -Count 1).CommandLine
  Write-Host "$ $last" -ForegroundColor DarkGray
  Invoke-Expression $last 2>&1 | errlens
}
# <<< errlens shell integration <<<
""".strip()

_SNIPPETS = {
    "bash": (_BASH_ZSH, "~/.bashrc"),
    "zsh": (_BASH_ZSH, "~/.zshrc"),
    "powershell": (_POWERSHELL, "$PROFILE"),
}


def _detect_shell() -> str:
    """Best-effort guess of the current shell."""
    import os

    if os.environ.get("PSModulePath"):
        return "powershell"
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return "zsh"
    return "bash"


def run(shell: str | None) -> int:
    """Print the integration snippet for the given (or detected) shell."""
    shell = (shell or _detect_shell()).lower()
    if shell not in _SNIPPETS:
        print(
            f"errlens: unknown shell '{shell}'. "
            f"Choose one of: {', '.join(_SNIPPETS)}",
            file=sys.stderr,
        )
        return 2

    snippet, rc_file = _SNIPPETS[shell]
    print(f"# Add the following to {rc_file}, then restart your shell:\n")
    print(snippet)
    print(f"\n# Afterwards: run a command, let it fail, then type 'err'.")
    return 0
