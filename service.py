"""Business logic used by the API (and by demo/tests): create job, add resume, delete candidate."""
import json
import uuid
from pathlib import Path

from cleaner import get_email, get_experience_years, get_name
from database import audit, get_conn, now
from extractor import extract_text
from redact import redact_pii
from skills import extract_skills


def create_job(title, jd_text, must_have, nice_to_have=(), min_exp_years=2.0, location=None, db_path=None):
    job_id = str(uuid.uuid4())
    with get_conn(db_path) as con:
        con.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)",
                    (job_id, title, jd_text, json.dumps([s.lower() for s in must_have]),
                     json.dumps([s.lower() for s in nice_to_have]), min_exp_years, location, now()))
        audit(con, "job_create", job_id)
    return job_id


def add_resume(file_path, candidate_id=None, db_path=None):
    """Extract text, parse it, redact contact details, store candidate + resume."""
    file_path = Path(file_path)
    raw = extract_text(file_path)
    candidate_id = candidate_id or str(uuid.uuid4())
    name = get_name(raw, file_path.stem)
    email = get_email(raw)
    safe_text = redact_pii(raw)                       # only redacted text is stored
    parsed = {"skills": extract_skills(raw), "years_exp": get_experience_years(raw)}
    with get_conn(db_path) as con:
        con.execute("INSERT OR REPLACE INTO candidates(id,name,email) VALUES (?,?,?)",
                    (candidate_id, name, email))
        con.execute("INSERT OR REPLACE INTO resumes VALUES (?,?,?,?,?)",
                    (candidate_id, file_path.suffix.lstrip(".").lower(), safe_text, json.dumps(parsed), now()))
        audit(con, "resume_upload", candidate_id)
    return {"candidate_id": candidate_id, "name": name, "skills": sorted(parsed["skills"]),
            "years_exp": parsed["years_exp"]}


def delete_candidate(candidate_id, db_path=None):
    """Right to deletion: remove everything stored about a candidate."""
    with get_conn(db_path) as con:
        for table, col in [("features", "candidate_id"), ("rankings", "candidate_id"),
                           ("resumes", "candidate_id"), ("candidates", "id")]:
            con.execute(f"DELETE FROM {table} WHERE {col}=?", (candidate_id,))
        audit(con, "candidate_delete", candidate_id)
