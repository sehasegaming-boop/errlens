# Recording the demo GIF

A short terminal cast is the single most effective thing for traction. Below are
two recipes — pick the one that matches your platform.

## Windows (recommended): ScreenToGif

[ScreenToGif](https://www.screentogif.com/) is a free GUI recorder that captures
a screen region straight to an optimized GIF — no terminal tooling required.

```powershell
# Install once
winget install NickeManarin.ScreenToGif
```

1. Open **Windows Terminal**, size it to roughly 90x24, and clear the screen.
2. Launch ScreenToGif and choose **Recorder**. Drag the capture frame over the
   terminal window.
3. Hit record, then run this focused sequence, pausing briefly between steps:

   ```powershell
   errlens doctor
   git push                                   # let it fail
   git push 2>&1 | errlens
   errlens "ModuleNotFoundError: No module named 'requests'"
   ```

4. Stop the recording. In the editor, trim dead air, then
   **File -> Save as -> Gif** to `docs/demo.gif`.

## macOS / Linux: asciinema + agg

```bash
pipx install asciinema
asciinema rec demo.cast --cols 90 --rows 24
# run the same sequence, then Ctrl-D
cargo install --git https://github.com/asciinema/agg
agg demo.cast docs/demo.gif --theme monokai --font-size 16
```

## Reference it in the README

The README already points at `docs/demo.gif`:

```markdown
![errlens demo](docs/demo.gif)
```

Drop the file there, commit, and it appears automatically.

## Tips

- Keep it under 25 seconds — attention drops fast.
- Show one clear failure -> explanation cycle; do not overload it.
- Use a small, fast model (`qwen2.5:3b`) so the wait reads as snappy.
- Run inside Windows Terminal for clean colors.
