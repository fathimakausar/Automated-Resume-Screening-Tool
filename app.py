"""Optional Streamlit dashboard:  streamlit run app.py
Upload resumes + paste a job description -> get a ranked table and CSV download."""
import tempfile
from pathlib import Path

import streamlit as st

from extractor import extract_text
from scorer import screen_resumes

st.set_page_config(page_title="Resume Screening Tool", layout="wide")
st.title("Automated Resume Screening Tool")

job_text = st.text_area("Job description", height=200,
                        value=Path("job_description.txt").read_text(encoding="utf-8"))
must = st.text_input("Must-have skills (comma separated)", "python, pandas, sql, excel")
nice = st.text_input("Nice-to-have skills (comma separated)", "power bi, tableau, matplotlib, statistics, git")
min_years = st.number_input("Minimum years of experience", 0.0, 20.0, 2.0, 0.5)
files = st.file_uploader("Upload resumes (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"],
                         accept_multiple_files=True)

if st.button("Screen resumes") and files:
    resumes = {}
    for f in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(f.name).suffix) as tmp:
            tmp.write(f.getbuffer())
        resumes[f.name] = extract_text(tmp.name)
    cfg = {"must_have": [s.strip() for s in must.split(",") if s.strip()],
           "nice_to_have": [s.strip() for s in nice.split(",") if s.strip()],
           "min_exp_years": min_years}
    df = screen_resumes(resumes, job_text, cfg)
    st.subheader("Ranking")
    st.dataframe(df[["rank", "candidate", "score", "must_have_coverage",
                     "years_experience", "decision", "reason"]], use_container_width=True)
    st.bar_chart(df.set_index("candidate")["score"])
    st.download_button("Download CSV report", df.to_csv(index=False), "ranking_report.csv")
elif st.button("Screen resumes (no files)"):
    st.warning("Please upload at least one resume.")
