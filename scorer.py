"""Phases 7-9 - skill matching, TF-IDF similarity, final score, decision, ranking."""
import pandas as pd
import config
from cleaner import clean_text, get_email, get_experience_years, get_name
from features import similarity, tfidf_similarity  # noqa: F401
from skills import extract_skills


def screen_resumes(resumes: dict, job_text: str, job_cfg: dict) -> pd.DataFrame:
    must = [s.lower() for s in job_cfg["must_have"]]
    nice = [s.lower() for s in job_cfg.get("nice_to_have", [])]
    min_years = float(job_cfg.get("min_exp_years", 0))
    w = config.WEIGHTS

    files = list(resumes)
    sims, sim_cap = similarity(job_text, [resumes[f] for f in files])

    rows = []
    for fname, sim in zip(files, sims):
        raw = resumes[fname]
        skills = extract_skills(raw)
        matched_must = [s for s in must if s in skills]
        missing_must = [s for s in must if s not in skills]
        matched_nice = [s for s in nice if s in skills]
        years = get_experience_years(raw)

        must_cov = len(matched_must) / len(must) if must else 1.0
        nice_cov = len(matched_nice) / len(nice) if nice else 0.0
        exp_score = min(1.0, years / min_years) if min_years else 1.0
        sim_scaled = min(1.0, sim / sim_cap)

        score = 100 * (w["text_similarity"] * sim_scaled + w["must_have"] * must_cov
                       + w["nice_to_have"] * nice_cov + w["experience"] * exp_score)

        # Flags - these make the decision explainable
        flags = []
        if missing_must:
            flags.append("Missing must-have: " + ", ".join(missing_must))
        if years < min_years:
            flags.append(f"Experience {years:g} yrs < required {min_years:g}")
        mentions = sum(skills.values())
        if skills and mentions / len(skills) > 2.5 and years == 0:
            flags.append("Possible keyword stuffing")

        shortlisted = score >= config.SHORTLIST_SCORE and must_cov >= config.MIN_MUST_HAVE_COVERAGE
        rows.append({
            "candidate": get_name(raw, fname),
            "file": fname,
            "email": get_email(raw),
            "score": round(score, 1),
            "text_similarity": round(sim, 3),
            "must_have_coverage": f"{len(matched_must)}/{len(must)}",
            "matched_skills": ", ".join(sorted(skills)),
            "missing_must_have": ", ".join(missing_must) or "None",
            "years_experience": years,
            "decision": "SHORTLIST" if shortlisted else "REJECT",
            "reason": "; ".join(flags) if flags else "Meets all must-have skills and experience",
        })

    df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df
