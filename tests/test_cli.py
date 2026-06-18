import io

import pytest

from errlens import cli


@pytest.fixture
def fake_explain(monkeypatch):
    """Replace the network call with a canned reply."""
    calls = {}

    def _explain(system, prompt, model):
        calls["model"] = model
        calls["prompt"] = prompt
        return "WHAT: x\nWHY: y\nHOW TO FIX: z"

    monkeypatch.setattr(cli, "explain", _explain)
    return calls


def test_explain_from_argument(monkeypatch, capsys, fake_explain):
    # Force the non-streaming path.
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False)
    rc = cli.main(["some error text"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "WHAT" in out and "HOW TO FIX" in out
    assert "some error text" in fake_explain["prompt"]


def test_custom_model_flag(monkeypatch, capsys, fake_explain):
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False)
    cli.main(["-m", "llama3.2:3b", "boom"])
    assert fake_explain["model"] == "llama3.2:3b"


def test_no_input_returns_usage_error(monkeypatch, capsys):
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: True)
    rc = cli.main([])
    err = capsys.readouterr().err
    assert rc == 2
    assert "No error text" in err


def test_stdin_is_read(monkeypatch, capsys, fake_explain):
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(cli.sys.stdin, "read", lambda: "piped error")
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False)
    rc = cli.main([])
    assert rc == 0
    assert "piped error" in fake_explain["prompt"]


def test_ollama_error_is_reported(monkeypatch, capsys):
    from errlens.ollama_client import OllamaError

    def _boom(*a, **k):
        raise OllamaError("ollama is down")

    monkeypatch.setattr(cli, "explain", _boom)
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False)
    rc = cli.main(["x"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "ollama is down" in err
