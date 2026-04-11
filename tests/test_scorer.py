"""Tests for src.analyzer and src.scorer (Phase 8 – JD matching)."""

import unittest

from src.analyzer import analyze_resume
from src.scorer import score


# ── Shared fixtures ───────────────────────────────────────────────────

CATALOG = {
    "categories": [
        {"name": "programming", "keywords": ["Python", "JavaScript", "SQL"]},
        {"name": "ml", "keywords": ["machine learning", "NLP", "PyTorch"]},
    ]
}


# ── Analyzer tests ────────────────────────────────────────────────────


class TestAnalyzer(unittest.TestCase):
    def test_matched_and_missing(self):
        resume = "python sql machine learning"
        jd = "python javascript machine learning nlp"
        out = analyze_resume(resume, jd, CATALOG)
        self.assertIn("python", out["matched_skills"])
        self.assertIn("machine learning", out["matched_skills"])
        self.assertIn("javascript", out["missing_skills"])
        self.assertIn("nlp", out["missing_skills"])

    def test_resume_skills_extracted(self):
        resume = "python python sql"
        jd = "python"
        out = analyze_resume(resume, jd, CATALOG)
        self.assertEqual(out["resume_skills"]["python"], 2)
        self.assertEqual(out["resume_skills"]["sql"], 1)

    def test_jd_skills_extracted(self):
        resume = "python"
        jd = "python javascript sql nlp"
        out = analyze_resume(resume, jd, CATALOG)
        self.assertEqual(len(out["jd_skills"]), 4)

    def test_no_overlap(self):
        resume = "python sql"
        jd = "nlp pytorch"
        out = analyze_resume(resume, jd, CATALOG)
        self.assertEqual(out["matched_skills"], [])
        self.assertEqual(sorted(out["missing_skills"]), ["nlp", "pytorch"])

    def test_full_overlap(self):
        resume = "python javascript sql"
        jd = "python sql"
        out = analyze_resume(resume, jd, CATALOG)
        self.assertEqual(sorted(out["matched_skills"]), ["python", "sql"])
        self.assertEqual(out["missing_skills"], [])

    def test_empty_jd(self):
        resume = "python sql"
        jd = ""
        out = analyze_resume(resume, jd, CATALOG)
        self.assertEqual(out["jd_skills"], {})
        self.assertEqual(out["matched_skills"], [])
        self.assertEqual(out["missing_skills"], [])


# ── Scorer tests ──────────────────────────────────────────────────────


class TestScorer(unittest.TestCase):
    def test_full_match(self):
        analysis = {
            "resume_skills": {"python": 1, "sql": 1},
            "jd_skills": {"python": 1, "sql": 1},
            "matched_skills": ["python", "sql"],
            "missing_skills": [],
        }
        out = score(analysis)
        self.assertEqual(out["overall_score"], 100)
        self.assertEqual(out["match_percentage"], 100.0)
        self.assertIn("Strong fit", out["feedback"])

    def test_partial_match(self):
        analysis = {
            "resume_skills": {"python": 1},
            "jd_skills": {"python": 1, "sql": 1, "javascript": 1},
            "matched_skills": ["python"],
            "missing_skills": ["sql", "javascript"],
        }
        out = score(analysis)
        self.assertEqual(out["overall_score"], 33)
        self.assertIn("Poor fit", out["feedback"])

    def test_no_match(self):
        analysis = {
            "resume_skills": {},
            "jd_skills": {"python": 1, "sql": 1},
            "matched_skills": [],
            "missing_skills": ["python", "sql"],
        }
        out = score(analysis)
        self.assertEqual(out["overall_score"], 0)
        self.assertIn("No match", out["feedback"])

    def test_empty_jd_skills(self):
        analysis = {
            "resume_skills": {"python": 1},
            "jd_skills": {},
            "matched_skills": [],
            "missing_skills": [],
        }
        out = score(analysis)
        self.assertEqual(out["overall_score"], 0)
        self.assertEqual(out["match_percentage"], 0.0)

    def test_score_capped_at_100(self):
        analysis = {
            "resume_skills": {"a": 1},
            "jd_skills": {"a": 1},
            "matched_skills": ["a"],
            "missing_skills": [],
        }
        out = score(analysis)
        self.assertLessEqual(out["overall_score"], 100)

    def test_details_structure(self):
        analysis = {
            "resume_skills": {"python": 1},
            "jd_skills": {"python": 1, "sql": 1},
            "matched_skills": ["python"],
            "missing_skills": ["sql"],
        }
        out = score(analysis)
        self.assertIn("matched_skills", out["details"])
        self.assertIn("missing_skills", out["details"])
        self.assertEqual(out["details"]["matched_skills"], ["python"])
        self.assertEqual(out["details"]["missing_skills"], ["sql"])


if __name__ == "__main__":
    unittest.main()
