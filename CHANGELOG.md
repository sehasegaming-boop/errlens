# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Streaming responses so tokens appear as the model generates them.
- `errlens doctor` to verify Ollama connectivity and model availability.
- `errlens install-hook` with an `err` shortcut for bash, zsh, and PowerShell
  that re-runs the previous command and explains its output.
- Test suite (pytest) and GitHub Actions CI across Python 3.10–3.12.

### Fixed
- Enable virtual terminal processing on Windows so colored output renders
  instead of printing raw ANSI escape codes; color is disabled automatically
  when the console cannot support it.

## [0.1.0] - 2026-06-18

### Added
- Initial MVP: explain piped or argument error text via a local Ollama model.
- Three-section output (What / Why / How to fix) with colored headers.
- Zero runtime dependencies (standard library only).
