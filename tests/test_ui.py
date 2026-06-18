from errlens import ui


def test_colorize_sections_wraps_known_headers():
    text = "WHAT: a thing\nWHY: a cause\nHOW TO FIX: do it"
    out = ui.colorize_sections(text)
    assert ui.SECTION_COLORS["WHAT"] in out
    assert ui.SECTION_COLORS["WHY"] in out
    assert ui.SECTION_COLORS["HOW TO FIX"] in out
    assert ui.RESET in out


def test_colorize_sections_leaves_other_lines_untouched():
    text = "just a normal line"
    assert ui.colorize_sections(text) == text


def test_supports_color_respects_no_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert ui.supports_color() is False


def test_style_disabled_returns_plain():
    assert ui.style("x", ui.RED, enabled=False) == "x"
