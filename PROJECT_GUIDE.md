# Automated Resume Screening Tool - Complete Project Guide

## 1. Project Explanation
**Simple:** A tool that reads many resumes and tells HR which ones match a job best - like a very fast first-round filter.

**Technical:** A Python NLP pipeline: extract text (pdfplumber / python-docx) -> clean with regex -> extract skills with a dictionary -> TF-IDF vectors -> cosine similarity with the job description -> weighted score -> rule-based shortlist/reject.

**Problem solved:** Manual screening of hundreds of resumes is slow, tiring and inconsistent.
**Why important:** Cuts time-to-hire, gives every resume the same checks, and lets recruiters spend time on interviews.
**How ATS works:** ATS tools look for keywords, skills, years of experience, education and job-description similarity, then rank and filter candidates.

**Workflow:** resume upload -> text extraction -> cleaning -> skill extraction -> job description matching -> score calculation -> shortlist/reject -> report

## 2. Tech Stack Options
| Option | Tools | Difficulty | Output |
|---|---|---|---|
| A - Easy | Python, regex, pandas, plain keyword counting | Easy | Keyword score + CSV |
| B - Intermediate (**chosen**) | + pdfplumber, python-docx, scikit-learn TF-IDF, cosine similarity, Streamlit (optional) | Medium | Ranked report, flags, chart, dashboard |
| C - Advanced | + spaCy, sentence-transformers, FastAPI, SQLite, Next.js dashboard | Hard | Semantic ranking, API, web UI |

**Best for students: Option B** - fully explainable, runs on a normal laptop, no heavy models. Option C items are listed as future improvements.

## 3. Architecture
```
INPUT                    PROCESSING                               OUTPUT
resumes (PDF/DOCX/TXT) -> extractor.py  (read text)            -> score /100
job description .txt   -> cleaner.py    (clean, name, years)   -> shortlisted list
job_config.json        -> skills.py     (skill extraction)     -> rejected list
(must-have skills)     -> scorer.py     (TF-IDF, cosine, rank) -> ranking CSV + chart
                       -> report.py     (save files)
```
**Data flow:** files -> raw text -> cleaned text -> skills + years -> similarity -> score -> decision -> DataFrame -> CSV/TXT/PNG.

**Score formula:** `100 x (0.40 x similarity + 0.35 x must-have coverage + 0.10 x nice-to-have coverage + 0.15 x experience ratio)`. Shortlist = score >= 60 AND at least 75% of must-have skills present.

## 4. Implementation Plan
| Phase | What to do | Why | Expected output | Beginner mistake |
|---|---|---|---|---|
| 1 Setup | Install Python, VS Code, Git | Working environment | `python --version` works | Forgetting "Add to PATH" |
| 2 Folders | Create structure in section 5 | GitHub-ready layout | Empty folders | Putting everything in one file |
| 3 Sample resumes | Run `generate_samples.py` | No real data available | 8 files in `resumes/` | Using real people's resumes |
| 4 Job description | Edit `data/job_description.txt` + `job_config.json` | Defines what "good" means | JD + skill lists | Vague must-have list |
| 5 Extraction | `src/extractor.py` | Parsing quality drives accuracy | Text per resume | Reading PDF as plain text |
| 6 Cleaning | `src/cleaner.py` | Removes noise | Clean lowercase text | Deleting `c++` / `c#` by mistake |
| 7 Skill matching | `src/skills.py` | Finds required skills | Skills + counts | Matching "C" inside other words |
| 8 Scoring | `src/scorer.py` | One comparable number | Score out of 100 | Trusting raw TF-IDF values |
| 9 Ranking | sort + decision rules | Shortlist/reject | Ranked table | Ignoring missing must-haves |
| 10 Reports | `src/report.py` | Evidence for HR | CSV, TXT, PNG | Not saving outputs |
| 11 GitHub | Section 10 | Proof of work | Public repo | Uploading `venv/` |

## 5. Folder Structure
- `resumes/` - input resumes (PDF/DOCX/TXT)
- `data/` - job description and job config
- `src/` - all logic, one file per task
- `outputs/` - generated reports
- `images/` - ranking chart + your screenshots
- `docs/` - this guide, sample terminal output
- `README.md`, `requirements.txt`, `.gitignore`, `main.py` (entry point), `app.py` (optional dashboard)

## 6. Installation Guide
1. Install Python 3.10+ from python.org (tick "Add Python to PATH").
2. Open terminal in the project folder.
3. **Windows:** `python -m venv venv` then `venv\Scripts\activate`
   **Mac:** `python3 -m venv venv` then `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Check: `python -c "import sklearn, pdfplumber, docx; print('OK')"`

## 8. Virtual Simulation (acting like a real HR system)
- **Sample resumes:** `generate_samples.py` writes 8 fake resumes on purpose covering different cases: two strong analysts, a developer missing Excel/pandas, a fresher, a Java developer, an HR executive, a senior BI analyst without Python, and a keyword-stuffed resume.
- **Job description:** "Junior Data Analyst (Python)" with responsibilities, requirements and nice-to-haves.
- **Required skills:** must-have = python, pandas, sql, excel; nice-to-have = power bi, tableau, matplotlib, statistics, git; minimum 2 years.
- **Text extraction:** pdfplumber for PDF, python-docx for DOCX, plain read for TXT.
- **Score:** TF-IDF similarity + skill coverage + experience, see section 3.
- **Ranking and decision:** sort by score; shortlist only if score >= 60 and must-have coverage >= 75%.
- **Capture:** terminal output, `outputs/ranking_report.csv`, `outputs/shortlisted_candidates.csv`, `images/ranking_chart.png`.
- **Upload to GitHub:** code, sample resumes, `outputs/`, `images/`, README.

## 9. How to Run
```bash
python generate_samples.py
python main.py
streamlit run app.py   # optional
```
Expected terminal output (see `docs/sample_terminal_output.txt`): 8 resumes extracted, ranked table, then "Shortlisted candidates: #1 Aarav Mehta 77.3/100, #2 Sneha Iyer 71.9/100".
CSV columns: rank, candidate, file, email, score, text_similarity, must_have_coverage, matched_skills, missing_must_have, years_experience, decision, reason.

## 10. GitHub Upload Steps
1. github.com -> New repository -> name `Automated-Resume-Screening-Tool`, Public, no README (you already have one).
2. In the project folder:
```bash
git init
git add .
git commit -m "Initial commit: resume screening project structure"
git branch -M main
git remote add origin https://github.com/<your-username>/Automated-Resume-Screening-Tool.git
git push -u origin main
```
3. Later changes: `git add .` -> `git commit -m "message"` -> `git push`.
4. **Description:** "Python NLP tool that screens resumes against a job description using TF-IDF, skill matching and ranking, with shortlist reports."
5. **Topics:** python, nlp, resume-screening, tf-idf, cosine-similarity, pandas, scikit-learn, hr-tech, streamlit, automation

## 12. Proof-Building Plan
| Day | Work | Commit message | Screenshot |
|---|---|---|---|
| 1 | Setup, folders, requirements, .gitignore | `Add project structure and requirements` | Folder structure |
| 2 | Sample resumes + extractor | `Add sample resumes and text extraction` | Resumes folder, extracted text |
| 3 | Cleaner, skills, JD matching | `Add cleaning, skill extraction and JD matching` | Matched skills output |
| 4 | Scoring and ranking | `Add TF-IDF scoring and ranking` | Terminal ranking table |
| 5 | Reports and chart | `Add CSV/TXT reports and ranking chart` | CSV, chart |
| 6 | README, docs, polish | `Add README and documentation` | GitHub repo page |

## 13. Screenshots to Capture
1. Project folder in VS Code  2. `resumes/` folder with the 8 files  3. Terminal after `python main.py`  4. The ranking table  5. `outputs/shortlisted_candidates.csv` opened in Excel  6. `outputs/ranking_report.csv`  7. `images/ranking_chart.png`  8. GitHub repo home page with README visible. Save into `images/` (except the GitHub one).

## 14. Interview Preparation
1. **Explain your project.** I built a Python tool that screens resumes against a job description. It extracts text from PDF/DOCX/TXT, cleans it, finds skills, compares each resume with the job description using TF-IDF and cosine similarity, calculates a score out of 100, flags missing must-have skills, and produces a ranked shortlist and CSV report. *HR view:* it saves hours of manual reading. *Technical view:* it is a hybrid of vector similarity and rule-based checks.
2. **What problem does it solve?** Manual resume filtering is slow and inconsistent; the tool gives a fast, uniform first screen.
3. **Which technologies did you use?** Python, pdfplumber, python-docx, regex, pandas, scikit-learn (TF-IDF, cosine similarity), matplotlib, optional Streamlit.
4. **How does it screen resumes?** Extract -> clean -> extract skills and years -> TF-IDF similarity with the JD -> weighted score -> shortlist only if score >= 60 and 75% of must-haves are present.
5. **What is TF-IDF and why use it?** It turns text into numbers, giving high weight to words that are frequent in a document but rare across documents. I used `sublinear_tf` so repeating a word many times does not inflate the score.
6. **What is cosine similarity?** It measures the angle between two vectors; closer to 1 means more similar text. I compare the job description vector with each resume vector.
7. **What output does it generate?** Ranked CSV, shortlisted and rejected CSVs, a text summary, a bar chart, and reasons such as "Missing must-have: python, pandas".
8. **What challenges did you face?** Different file formats, noisy text, skill aliases (sklearn vs scikit-learn), low raw TF-IDF values (solved by scaling), and keyword stuffing (solved with sublinear TF, an experience check and a stuffing flag).
9. **How can it be improved?** Semantic embeddings, education and experience extraction using NLP, FastAPI backend, recruiter dashboard, database, bias audits.
10. **Explain to a non-technical person.** It is a tool that reads resumes for you and shows which candidates fit the job best, so recruiters can shortlist faster.

**Bonus - fairness:** The tool never uses gender, age, religion or caste. It gives skills-based reasons, and a human recruiter makes the final decision.

*Note: section 7 (full code) and section 11 (README) are in the repository files: `src/`, `main.py`, `app.py`, `README.md`.*

## 15. Advanced Version (Database, FastAPI, Next.js, Evaluation, Compliance)
The project brief's step-by-step section is implemented in the same repository:
- **Step 2 Data schema:** `db/schema.sql`, `src/database.py`
- **Step 3 Ingestion/parsing:** `src/extractor.py`, `src/service.py`
- **Step 4 Skill extraction:** `src/skills.py`, `src/cleaner.py` (dictionary + regex)
- **Step 5 Features:** `src/features.py` (TF-IDF, optional embeddings)
- **Step 6 Scoring and reasons:** `src/scorer.py`, `src/rank.py`
- **Step 7 Evaluation:** `evaluation/evaluate.py` (ROC-AUC 0.867, PR-AUC 0.867 on the toy set)
- **Step 8 FastAPI:** `api/app.py`
- **Step 9 Next.js dashboard:** `web/`
- **Step 10 Compliance and deployment:** `src/redact.py`, delete endpoint, audit log, Dockerfiles, docker-compose

Run: `python demo_db.py`, `uvicorn api.app:app --reload`, then `cd web && npm install && npm run dev`.
