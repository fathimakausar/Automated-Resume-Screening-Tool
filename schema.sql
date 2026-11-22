-- SQLite schema (lists such as must_have are stored as JSON text)
CREATE TABLE IF NOT EXISTS jobs(
  id TEXT PRIMARY KEY,
  title TEXT, jd_text TEXT,
  must_have TEXT, nice_to_have TEXT,
  min_exp_years REAL, location TEXT,
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS candidates(
  id TEXT PRIMARY KEY,
  name TEXT, email TEXT, phone TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS resumes(
  candidate_id TEXT PRIMARY KEY REFERENCES candidates(id),
  source TEXT,          -- pdf / docx / txt
  raw_text TEXT,        -- text with email/phone redacted
  parsed_json TEXT,     -- skills, years of experience
  updated_at TEXT
);
CREATE TABLE IF NOT EXISTS features(
  candidate_id TEXT REFERENCES candidates(id),
  job_id TEXT REFERENCES jobs(id),
  sim_embedding REAL,   -- similarity 0..1
  rule_musthave_hits INTEGER,
  rule_musthave_total INTEGER,
  years_exp REAL,
  gap_penalty REAL,     -- share of must-have skills missing
  PRIMARY KEY(candidate_id, job_id)
);
CREATE TABLE IF NOT EXISTS rankings(
  job_id TEXT, candidate_id TEXT,
  rank INTEGER, score REAL, decision TEXT, reasons TEXT, created_at TEXT,
  PRIMARY KEY(job_id, candidate_id)
);
CREATE TABLE IF NOT EXISTS audit_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT, action TEXT, detail TEXT
);
