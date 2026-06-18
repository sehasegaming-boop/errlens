from errlens.prompt import SYSTEM_PROMPT, build_prompt


def test_system_prompt_requests_three_sections():
    upper = SYSTEM_PROMPT.upper()
    assert "WHAT" in upper
    assert "WHY" in upper
    assert "HOW TO FIX" in upper


def test_build_prompt_includes_and_strips_error_text():
    result = build_prompt("  ModuleNotFoundError: foo  ")
    assert "ModuleNotFoundError: foo" in result
    assert "ERROR OUTPUT" in result
    # Surrounding whitespace should be trimmed.
    assert "  ModuleNotFoundError" not in result
