"""FastAPI service.  Run from the project root:  uvicorn api:app --reload
Docs page: http://localhost:8000/docs"""
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import service
from database import get_conn, init_db, loads
from rank import get_rankings, rank_job

app = FastAPI(title="Automated Resume Screening API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"],
                   allow_methods=["*"], allow_headers=["*"])
init_db()

MAX_FILE_BYTES = 5 * 1024 * 1024
ALLOWED = {".pdf", ".docx", ".txt"}


class Job(BaseModel):
    title: str
    jd_text: str
    must_have: List[str] = []
    nice_to_have: List[str] = []
    min_exp_years: float = 2.0
    location: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/job/create")
def job_create(job: Job):
    job_id = service.create_job(job.title, job.jd_text, job.must_have, job.nice_to_have,
                                job.min_exp_years, job.location)
    return {"job_id": job_id}


@app.post("/resume/upload")
async def resume_upload(file: UploadFile = File(...), candidate_id: Optional[str] = Form(None)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED:
        raise HTTPException(400, "Only PDF, DOCX and TXT files are allowed")
    data = await file.read()
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(413, "File too large (max 5 MB)")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
    try:
        return {"ok": True, **service.add_resume(tmp.name, candidate_id)}
    except Exception as err:
        raise HTTPException(422, f"Could not parse resume: {err}")
    finally:
        os.unlink(tmp.name)


@app.post("/rank/{job_id}")
def rank(job_id: str):
    try:
        return rank_job(job_id)
    except KeyError:
        raise HTTPException(404, "Job not found")


@app.get("/rankings/{job_id}")
def rankings(job_id: str):
    return get_rankings(job_id)


@app.get("/explain/{job_id}/{candidate_id}")
def explain(job_id: str, candidate_id: str):
    for row in get_rankings(job_id):
        if row["candidate_id"] == candidate_id:
            return row
    raise HTTPException(404, "Ranking not found - run /rank first")


@app.delete("/candidate/{candidate_id}")
def candidate_delete(candidate_id: str):
    service.delete_candidate(candidate_id)
    return {"deleted": candidate_id}


@app.get("/audit")
def audit_log(limit: int = 50):
    with get_conn() as con:
        rows = con.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
