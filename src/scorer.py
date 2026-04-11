"""ATS-style scoring from analysis output."""

from __future__ import annotations

MAX_SCORE = 100


def score(analysis: dict) -> dict:
    """
    Compute an ATS match score from analyzer output.

    Core metric:
        match_percentage = matched / total_jd_skills × 100

    The overall_score mirrors match_percentage (capped at 100).

    Returns:
        overall_score    – int (0-100)
        match_percentage – float (0.0-100.0)
        feedback         – human-readable summary
        details          – {matched_skills: [...], missing_skills: [...]}
    """
    matched_skills = analysis.get("matched_skills", [])
    missing_skills = analysis.get("missing_skills", [])
    jd_skills = analysis.get("jd_skills", {})

    total_jd = len(jd_skills)

    # ── Match percentage ──────────────────────────────────────────────
    if total_jd > 0:
        match_pct = (len(matched_skills) / total_jd) * 100.0
    else:
        match_pct = 0.0

    overall = min(int(round(match_pct)), MAX_SCORE)

    # ── Feedback ──────────────────────────────────────────────────────
    feedback = _build_feedback(overall, missing_skills)

    return {
        "overall_score": overall,
        "match_percentage": round(match_pct, 2),
        "feedback": feedback,
        "details": {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        },
    }


# ── Helpers ────────────────────────────────────────────────────────────


def _build_feedback(overall: int, missing: list) -> str:
    """Return a one-liner feedback string based on score tier."""
    if overall >= 80:
        return "Strong fit — your resume aligns well with this job description."
    if overall >= 50:
        tip = ""
        if missing:
            tip = f" Consider adding: {', '.join(missing[:3])}."
        return f"Moderate fit — some relevant skills are present, but gaps remain.{tip}"
    if overall > 0:
        return "Poor fit — your resume is missing most skills listed in the job description."
    return "No match — the job description may not contain recognizable skills."
