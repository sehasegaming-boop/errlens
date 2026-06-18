# Contributing to errlens

Thanks for your interest in improving errlens! Contributions of all kinds are
welcome — bug reports, feature ideas, docs, and code.

## Development setup

```bash
git clone https://github.com/sehasegaming-boop/errlens
cd errlens
pip install -e ".[dev]"
```

## Running tests

```bash
pytest -q
```

The test suite does not require Ollama — network calls are mocked.

## Guidelines

- **English only** for code, identifiers, comments, output, and commits.
- **Keep it small and focused.** errlens does one thing well: explain errors.
  New features should justify their weight; avoid scope creep.
- **No runtime dependencies.** The CLI runs on the Python standard library.
  Dev/test-only dependencies are fine.
- Add or update tests for behavior changes.
- Follow the existing code style (PEP 8, type hints where they clarify intent).

## Commit messages

Write clear, imperative commit messages (e.g. "Add streaming output"). Reference
issues where relevant.

## Reporting bugs

Open an issue with the command you ran, the error text, your OS, Python version,
and the model you used (`errlens doctor` output is helpful).
