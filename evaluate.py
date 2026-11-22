"""Check ranking quality on a tiny labelled set (1 = recruiter would select, 0 = would not).
Run from the project root:  python evaluate.py"""
import json

import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

import config
from extractor import load_resumes
from scorer import screen_resumes

job_text = open(config.JOB_TEXT_FILE, encoding="utf-8").read()
job_cfg = json.load(open(config.JOB_CONFIG_FILE, encoding="utf-8"))

scores = screen_resumes(load_resumes(config.RESUME_DIR), job_text, job_cfg)[["file", "score", "decision"]]
df = scores.merge(pd.read_csv(config.DATA_DIR / "labeled_pairs.csv"), on="file")

k = 3
top_k = df.sort_values("score", ascending=False).head(k)
lines = [
    f"Labelled resumes     : {len(df)}",
    f"ROC-AUC              : {roc_auc_score(df.label, df.score):.3f}",
    f"PR-AUC               : {average_precision_score(df.label, df.score):.3f}",
    f"Top-{k} precision      : {top_k.label.mean():.3f}",
    f"Shortlist precision  : {df[df.decision == 'SHORTLIST'].label.mean():.3f}",
    f"Shortlist recall     : {df[df.label == 1].decision.eq('SHORTLIST').mean():.3f}",
]
lines.append("Sanity: every candidate missing a must-have shows a warning -> "
             + str(all(('Missing' in r) for r in screen_resumes(load_resumes(config.RESUME_DIR), job_text, job_cfg)
                       .query("missing_must_have != 'None'").reason)))
print("\n".join(lines))
(config.OUTPUT_DIR / "evaluation.txt").write_text("\n".join(lines), encoding="utf-8")
