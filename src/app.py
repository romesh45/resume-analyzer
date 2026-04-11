"""Web application entry point for the Resume Analyzer."""

import json
from pathlib import Path

from flask import Flask, render_template, request

from src.analyzer import analyze_resume
from src.preprocess import extract_text, normalize_text
from src.scorer import score

_BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=str(_BASE_DIR / "templates"))

SKILLS_PATH = _BASE_DIR / "data" / "skills.json"


def _load_skills_catalog() -> dict:
    """Load the skills catalog from disk."""
    with open(SKILLS_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        resume_file = request.files.get("resume_file")
        resume_raw = request.form.get("resume_text", "")
        jd_raw = request.form.get("job_description", "")

        try:
            # Handle PDF upload if a file was selected
            if resume_file and resume_file.filename:
                resume_raw = extract_text(resume_file)

            if not resume_raw.strip():
                error = "No text found. Please paste your resume or upload a text-based PDF."
            elif not jd_raw.strip():
                error = "Please provide a job description to compare against."

            if not error:
                resume_clean = normalize_text(resume_raw)
                jd_clean = normalize_text(jd_raw)

                catalog = _load_skills_catalog()
                analysis = analyze_resume(resume_clean, jd_clean, catalog)
                result = score(analysis)
        except Exception as e:
            error = f"Error processing input: {str(e)}"

    return render_template("index.html", result=result, error=error)


def create_app():
    return app


if __name__ == "__main__":
    app.run(debug=True)
