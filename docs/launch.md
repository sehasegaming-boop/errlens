# Launch copy

Ready-to-paste posts for sharing errlens. Tweak the username/links as needed.

---

## Hacker News — Show HN

**Title:**
```
Show HN: errlens – explain terminal errors locally with Ollama (no cloud)
```

**Body:**
```
I kept copy-pasting stack traces into a browser to figure out what went wrong,
and I wasn't comfortable sending work error output to a cloud service. So I built
errlens: pipe a failed command's output to it, and it explains what the error is,
why it happened, and how to fix it — using a local Ollama model. Nothing leaves
your machine.

  some_command 2>&1 | errlens

It's tiny: pure Python standard library, zero runtime dependencies. There's an
`errlens doctor` to check your setup, and an `errlens install-hook` that adds an
`err` shortcut to explain the last failed command in bash/zsh/PowerShell.

Default model is qwen2.5:3b so it runs fine on CPU. Cloud backends are
deliberately not the default — local is the whole point.

Repo: https://github.com/sehasegaming-boop/errlens

Feedback welcome, especially on prompt quality and which models work best on CPU.
```

---

## Reddit — r/commandline, r/Python

**Title:**
```
errlens: a local-first CLI that explains terminal errors with Ollama (no data leaves your machine)
```

**Body:**
```
When a command fails, errlens reads the error output and tells you what it is,
why it happened, and how to fix it — all via a local Ollama model.

    some_command 2>&1 | errlens
    errlens "ModuleNotFoundError: No module named 'requests'"

- Privacy-first: 100% local, no cloud, no telemetry
- Zero runtime dependencies (Python stdlib only)
- `errlens doctor` checks your Ollama setup
- `errlens install-hook` adds an `err` shortcut for the last failed command

Runs on CPU with qwen2.5:3b by default. MIT licensed.

https://github.com/sehasegaming-boop/errlens

Would love feedback and contributors.
```

---

## X / Bluesky

```
Built errlens 🔍 — a local-first CLI that explains your terminal errors.

A command fails → it tells you what broke, why, and how to fix it.
Runs on a local Ollama model. Nothing leaves your machine.

  some_command 2>&1 | errlens

Pure Python, zero deps, MIT.
https://github.com/sehasegaming-boop/errlens
```

---

## Tips

- Post Show HN on a weekday morning (US time) for best visibility.
- Reply quickly to early comments — engagement drives ranking.
- Pin the demo (docs/demo.svg or a GIF) at the top of the README first.
