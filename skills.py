"""Skill dictionary + skill extraction using word-boundary regex matching."""
import re

# canonical skill -> list of ways it can be written in a resume
SKILL_DB = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "excel": ["excel", "ms excel", "advanced excel"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib", "seaborn"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "statistics": ["statistics", "statistical analysis", "hypothesis testing"],
    "machine learning": ["machine learning", "scikit-learn", "sklearn"],
    "git": ["git", "github"],
    "django": ["django"],
    "flask": ["flask"],
    "docker": ["docker"],
    "java": ["java"],
    "spring": ["spring boot", "spring"],
    "javascript": ["javascript"],
    "react": ["react", "reactjs"],
    "html/css": ["html", "css"],
    "aws": ["aws", "amazon web services"],
    "linux": ["linux"],
    "data visualization": ["data visualization", "data visualisation", "dashboards"],
    "communication": ["communication"],
    "recruitment": ["recruitment", "talent acquisition"],
}


def _pattern(alias: str) -> re.Pattern:
    # (?<![a-z0-9+#]) / (?![a-z0-9+#]) = "whole word" check that also works for c++, c#
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])")


_PATTERNS = {skill: [_pattern(a) for a in aliases] for skill, aliases in SKILL_DB.items()}


def extract_skills(text: str) -> dict:
    """Return {skill: number_of_mentions} for every skill found in the text."""
    text = text.lower()
    found = {}
    for skill, patterns in _PATTERNS.items():
        count = sum(len(p.findall(text)) for p in patterns)
        if count:
            found[skill] = count
    return found
