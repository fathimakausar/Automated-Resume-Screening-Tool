"""Database-driven ranking: score every stored resume for one job and save the results."""
import json

from database import audit, get_conn, loads, now
from scorer import screen_resumes


def rank_job(job_id, db_path=None):
    with get_conn(db_path) as con:
        job = con.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if job is None:
            raise KeyError(f"Job {job_id} not found")
        rows = con.execute("""SELECT c.id, c.name, c.email, r.raw_text FROM resumes r
                              JOIN candidates c ON c.id = r.candidate_id""").fetchall()
        if not rows:
            return []

        cfg = {"must_have": loads(job["must_have"], []), "nice_to_have": loads(job["nice_to_have"], []),
               "min_exp_years": job["min_exp_years"] or 0}
        df = screen_resumes({r["id"]: r["raw_text"] for r in rows}, job["jd_text"], cfg)
        info = {r["id"]: r for r in rows}

        results = []
        for _, r in df.iterrows():
            cid = r["file"]
            hits, total = (int(x) for x in r["must_have_coverage"].split("/"))
            reasons = {
                "must_have_coverage": r["must_have_coverage"],
                "missing_must_have": r["missing_must_have"],
                "matched_skills": r["matched_skills"],
                "years_experience": r["years_experience"],
                "similarity": r["text_similarity"],
                "explanation": r["reason"],
            }
            con.execute("""INSERT OR REPLACE INTO features VALUES (?,?,?,?,?,?,?)""",
                        (cid, job_id, r["text_similarity"], hits, total, r["years_experience"],
                         round(1 - hits / total, 3) if total else 0.0))
            con.execute("""INSERT OR REPLACE INTO rankings VALUES (?,?,?,?,?,?,?)""",
                        (job_id, cid, int(r["rank"]), float(r["score"]), r["decision"],
                         json.dumps(reasons), now()))
            results.append({"rank": int(r["rank"]), "candidate_id": cid, "name": info[cid]["name"],
                            "email": info[cid]["email"], "score": float(r["score"]),
                            "decision": r["decision"], "reasons": reasons})
        audit(con, "rank", f"job={job_id} candidates={len(results)}")
        return results


def get_rankings(job_id, db_path=None):
    with get_conn(db_path) as con:
        rows = con.execute("""SELECT g.*, c.name, c.email FROM rankings g
                              JOIN candidates c ON c.id = g.candidate_id
                              WHERE g.job_id=? ORDER BY g.rank""", (job_id,)).fetchall()
        return [{"rank": r["rank"], "candidate_id": r["candidate_id"], "name": r["name"],
                 "email": r["email"], "score": r["score"], "decision": r["decision"],
                 "reasons": loads(r["reasons"], {})} for r in rows]
