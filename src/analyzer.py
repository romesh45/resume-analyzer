"""NLP analysis: skills, entities, and keyword alignment."""

from __future__ import annotations

from typing import Any


def analyze_resume(
    resume_text: str,
    jd_text: str,
    skills_catalog: dict[str, Any],
) -> dict[str, Any]:
    """
    Compare a normalized resume against a normalized job description.

    Both texts are scanned for keywords defined in *skills_catalog*.
    The result highlights which JD-required skills the resume covers
    and which are missing.

    Returns:
        resume_skills  – {skill: frequency} found in the resume
        jd_skills      – {skill: frequency} found in the JD
        matched_skills – skills present in BOTH resume and JD
        missing_skills – skills in JD but NOT in resume
    """
    resume_skills = _extract_skills(resume_text, skills_catalog)
    jd_skills = _extract_skills(jd_text, skills_catalog)

    # Skills the JD asks for that the resume also contains
    matched_skills = sorted(
        skill for skill in jd_skills if skill in resume_skills
    )

    # Skills the JD asks for that the resume is missing
    missing_skills = sorted(
        skill for skill in jd_skills if skill not in resume_skills
    )

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


# ── Helpers ────────────────────────────────────────────────────────────


def _extract_skills(
    text: str, skills_catalog: dict[str, Any]
) -> dict[str, int]:
    """Return {skill_lower: count} for every catalog keyword found in *text*."""
    found: dict[str, int] = {}
    for category in skills_catalog.get("categories", []):
        for keyword in category.get("keywords", []):
            count = _count_occurrences(text, keyword.lower())
            if count > 0:
                found[keyword.lower()] = count
    return found


def _count_occurrences(text: str, keyword: str) -> int:
    """Count non-overlapping occurrences of *keyword* in *text*."""
    count = 0
    start = 0
    while True:
        idx = text.find(keyword, start)
        if idx == -1:
            break
        count += 1
        start = idx + len(keyword)
    return count
