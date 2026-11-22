"""Run the full screening pipeline:  python main.py"""
import argparse
import json

import pandas as pd

import config
from extractor import load_resumes
from report import save_chart, save_csv, save_text_report
from scorer import screen_resumes


def main():
    ap = argparse.ArgumentParser(description="Automated Resume Screening Tool")
    ap.add_argument("--resumes", default=str(config.RESUME_DIR), help="folder with resumes")
    ap.add_argument("--job", default=str(config.JOB_TEXT_FILE), help="job description .txt")
    ap.add_argument("--config", default=str(config.JOB_CONFIG_FILE), help="job config .json")
    args = ap.parse_args()

    job_text = open(args.job, encoding="utf-8").read()
    job_cfg = json.load(open(args.config, encoding="utf-8"))

    print(f"Job: {job_cfg['title']}")
    print(f"Must-have: {job_cfg['must_have']} | Min experience: {job_cfg['min_exp_years']} yrs\n")

    resumes = load_resumes(args.resumes)
    print(f"[1/4] Extracted text from {len(resumes)} resumes")
    df = screen_resumes(resumes, job_text, job_cfg)
    print("[2/4] Skills matched, scores calculated, candidates ranked")

    csv_path = save_csv(df)
    txt_path = save_text_report(df, job_cfg["title"])
    img_path = save_chart(df, job_cfg["title"])
    print(f"[3/4] Reports saved: {csv_path.name}, {txt_path.name}, {img_path.name}\n")

    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 45)
    print(df[["rank", "candidate", "score", "must_have_coverage", "years_experience", "decision"]]
          .to_string(index=False))
    print("\n[4/4] Shortlisted candidates:")
    for _, r in df[df.decision == "SHORTLIST"].iterrows():
        print(f"  #{r['rank']} {r['candidate']} - {r['score']}/100")


if __name__ == "__main__":
    main()
