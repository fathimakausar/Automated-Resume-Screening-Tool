"""Phase 6 - text cleaning + simple field extraction (name, email, experience)."""
import re


def clean_text(text: str) -> str:
    """Lowercase, remove emails/phones/urls/special characters, squeeze spaces."""
    text = text.lower()
    text = re.sub(r"\S+@\S+", " ", text)                    # emails
    text = re.sub(r"http\S+|www\.\S+", " ", text)           # links
    text = re.sub(r"\+?\d[\d\s\-()]{8,}\d", " ", text)      # phone numbers
    text = re.sub(r"[^a-z0-9+#\s]", " ", text)              # keep letters, digits, c++/c#
    return re.sub(r"\s+", " ", text).strip()


def get_name(raw: str, fallback: str) -> str:
    for line in raw.splitlines():
        line = line.strip()
        if line:
            return line.title() if len(line.split()) <= 4 else fallback
    return fallback


def get_email(raw: str) -> str:
    m = re.search(r"[\w.\-+]+@[\w\-]+\.[\w.\-]+", raw)
    return m.group(0) if m else ""


def get_experience_years(raw: str) -> float:
    """Estimate years of experience.
    1) look for phrases like '3 years' / '2+ yrs'
    2) else add up month phrases like '6 months'
    3) else add up year ranges like '2019 - 2022' or '2021 - present'"""
    text = raw.lower()
    years = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|year|yrs|yr)\b", text)]
    if years:
        return max(years)
    months = [float(x) for x in re.findall(r"(\d+)\s*\+?\s*months?\b", text)]
    if months:
        return round(sum(months) / 12, 1)
    total = 0.0
    for start, end in re.findall(r"((?:19|20)\d{2})\s*(?:-|–|to)\s*((?:19|20)\d{2}|present)", text):
        end_year = 2026 if end == "present" else int(end)
        total += max(0, end_year - int(start))
    return float(total)
