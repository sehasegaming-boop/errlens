# Recording the demo GIF

A short terminal cast is the single most effective thing for traction. Here is
the exact recipe used for the README demo.

## 1. Record with asciinema

```bash
# Install once
pipx install asciinema        # or: pip install asciinema

# Record a focused, ~20 second session
asciinema rec demo.cast --cols 90 --rows 24
```

Run this scripted sequence inside the recording, pausing briefly between steps:

```bash
errlens doctor
git push                                  # let it fail
git push 2>&1 | errlens
errlens "ModuleNotFoundError: No module named 'requests'"
```

Press `Ctrl-D` (or type `exit`) to stop recording.

## 2. Convert the cast to a GIF

```bash
# agg is the official asciinema GIF generator
cargo install --git https://github.com/asciinema/agg
agg demo.cast docs/demo.gif --theme monokai --font-size 16
```

## 3. Reference it in the README

```markdown
![errlens demo](docs/demo.gif)
```

## Tips

- Keep it under 25 seconds — attention drops fast.
- Show one clear failure → explanation cycle; do not overload it.
- Use a small, fast model (`qwen2.5:3b`) so the wait reads as snappy.
- Trim dead air in the `.cast` JSON if a CPU response was slow.
