"""Central settings: folder paths, scoring weights and decision rules.
Change values here to tune the screening behaviour - no other file needs editing."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESUME_DIR = BASE_DIR / "resumes"
DATA_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "outputs"
IMAGE_DIR = BASE_DIR / "images"

JOB_TEXT_FILE = DATA_DIR / "job_description.txt"   # full job description (free text)
JOB_CONFIG_FILE = DATA_DIR / "job_config.json"     # title, must-have skills, min experience

# ---- Score = weighted sum of 4 parts (weights must add up to 1.0) ----
WEIGHTS = {
    "text_similarity": 0.40,   # TF-IDF + cosine similarity of resume vs job description
    "must_have": 0.35,         # share of must-have skills found
    "nice_to_have": 0.10,      # share of nice-to-have skills found
    "experience": 0.15,        # years of experience vs required years
}

# Raw TF-IDF cosine values are usually small (0.1 - 0.5) even for good matches,
# so we scale them: similarity of 0.50 or more counts as a full 1.0.
SIMILARITY_CAP = 0.50

# ---- Decision rules ----
SHORTLIST_SCORE = 60.0        # minimum final score (out of 100)
MIN_MUST_HAVE_COVERAGE = 0.75  # at least 75% of must-have skills must be present

# ---- Advanced options (FastAPI / database / embeddings) ----
import os
DB_PATH = Path(os.getenv("RESUME_DB", BASE_DIR / "screening.db"))
SCHEMA_FILE = BASE_DIR / "schema.sql"
# "tfidf" (default, no download needed) or "embeddings" (sentence-transformers, all-MiniLM-L6-v2)
SIMILARITY_BACKEND = os.getenv("SIMILARITY_BACKEND", "tfidf")
EMBEDDING_SIMILARITY_CAP = 0.60
