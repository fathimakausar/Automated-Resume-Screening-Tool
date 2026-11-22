"""Simple tests.  Run from the project root:  python test_core.py"""
import json

import config, service
from cleaner import get_experience_years
from database import init_db
from extractor import load_resumes
from rank import get_rankings, rank_job
from redact import redact_pii
from scorer import screen_resumes
from skills import extract_skills


def test_skills():
    s = extract_skills("Worked with C++, Python and sklearn; plus javascripty")
    assert "python" in s and "machine learning" in s and "javascript" not in s


def test_experience():
    assert get_experience_years("3 years of experience") == 3
    assert get_experience_years("6 months internship") == 0.5
    assert get_experience_years("Analyst 2022 - 2024") == 2


def test_redaction():
    out = redact_pii("mail me at a.b@example.com or +91 90000 11111")
    assert "@" not in out and "90000" not in out


def test_pipeline_and_db(tmp_path=config.BASE_DIR / "test.db"):
    cfg = json.load(open(config.JOB_CONFIG_FILE))
    df = screen_resumes(load_resumes(config.RESUME_DIR), open(config.JOB_TEXT_FILE).read(), cfg)
    assert list(df[df.decision == "SHORTLIST"].candidate) == ["Aarav Mehta", "Sneha Iyer"]

    tmp_path.unlink(missing_ok=True)
    init_db(tmp_path)
    job_id = service.create_job(cfg["title"], open(config.JOB_TEXT_FILE).read(), cfg["must_have"],
                                cfg["nice_to_have"], cfg["min_exp_years"], db_path=tmp_path)
    ids = [service.add_resume(f, db_path=tmp_path)["candidate_id"] for f in sorted(config.RESUME_DIR.iterdir())]
    assert len(rank_job(job_id, tmp_path)) == 8
    service.delete_candidate(ids[0], tmp_path)
    assert len(get_rankings(job_id, tmp_path)) == 7
    tmp_path.unlink()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
