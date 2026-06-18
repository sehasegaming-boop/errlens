"""Build the prompt sent to the local model."""

SYSTEM_PROMPT = (
    "You are errlens, a terminal error explainer. "
    "Given the raw error output of a failed command, explain it concisely. "
    "Always answer in English using exactly these three sections, in order:\n"
    "WHAT: one or two sentences naming the error.\n"
    "WHY: the most likely cause, specific to the given output.\n"
    "HOW TO FIX: concrete, numbered steps the user can run.\n"
    "Do not add any other sections, preamble, or closing remarks. "
    "Keep it short and practical."
)


def build_prompt(error_text: str) -> str:
    """Wrap the captured error text into a user prompt."""
    error_text = error_text.strip()
    return (
        "Explain the following terminal error.\n\n"
        "--- ERROR OUTPUT ---\n"
        f"{error_text}\n"
        "--- END ---"
    )
