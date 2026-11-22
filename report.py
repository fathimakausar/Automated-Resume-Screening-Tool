"""Phase 10 - save CSV, text report and ranking chart."""
import matplotlib
matplotlib.use("Agg")           # no pop-up window needed
import matplotlib.pyplot as plt

import config


def save_csv(df, name="ranking_report.csv"):
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    path = config.OUTPUT_DIR / name
    df.to_csv(path, index=False)
    df[df.decision == "SHORTLIST"].to_csv(config.OUTPUT_DIR / "shortlisted_candidates.csv", index=False)
    df[df.decision == "REJECT"].to_csv(config.OUTPUT_DIR / "rejected_candidates.csv", index=False)
    return path


def save_text_report(df, job_title, name="screening_summary.txt"):
    lines = [f"RESUME SCREENING REPORT - {job_title}", "=" * 60,
             f"Total resumes screened : {len(df)}",
             f"Shortlisted            : {(df.decision == 'SHORTLIST').sum()}",
             f"Rejected               : {(df.decision == 'REJECT').sum()}", "", "RANKING", "-" * 60]
    for _, r in df.iterrows():
        lines.append(f"#{r['rank']} {r['candidate']:<18} {r['score']:>5}/100  {r['decision']:<9} | {r['reason']}")
    path = config.OUTPUT_DIR / name
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def save_chart(df, job_title, name="ranking_chart.png"):
    config.IMAGE_DIR.mkdir(exist_ok=True)
    d = df.iloc[::-1]
    colors = ["#2e9e5b" if x == "SHORTLIST" else "#d9534f" for x in d.decision]
    plt.figure(figsize=(9, 5))
    plt.barh(d.candidate, d.score, color=colors)
    plt.axvline(config.SHORTLIST_SCORE, color="grey", linestyle="--", label="Shortlist cut-off")
    plt.xlabel("Match score (out of 100)")
    plt.title(f"Resume ranking - {job_title}")
    plt.legend()
    plt.tight_layout()
    path = config.IMAGE_DIR / name
    plt.savefig(path, dpi=150)
    plt.close()
    return path
