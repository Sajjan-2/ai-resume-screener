import re

SKILLS_DB = [
    "python",
    "sql",
    "mysql",
    "mongodb",
    "power bi",
    "excel",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "machine learning",
    "deep learning",
    "html",
    "css",
    "javascript",
    "flask",
    "django",
    "git",
    "github",
]


def extract_skills(text):
    """
    Extracts skills using word-boundary regex matching instead of plain
    substring matching, to avoid false positives (e.g. "git" matching
    inside "digital").
    """
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills