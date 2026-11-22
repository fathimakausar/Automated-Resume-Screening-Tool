"""Privacy: remove emails and phone numbers before text is stored or sent to a model."""
import re


def redact_pii(text: str) -> str:
    text = re.sub(r"[\w.\-+]+@[\w\-]+\.[\w.\-]+", "[EMAIL]", text)
    text = re.sub(r"\+?\d[\d\s\-()]{8,}\d", "[PHONE]", text)
    return text
