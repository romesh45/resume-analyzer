"""Web application entry point for the Resume Analyzer."""

import json
from pathlib import Path

from flask import Flask, render_template, request, jsonify

from src.analyzer import analyze_resume
from src.preprocess import extract_text, normalize_text
from src.scorer import score

_BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=str(_BASE_DIR / "templates"))
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit

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
            if resume_file and resume_file.filename:
                resume_raw = extract_text(resume_file)

            if not resume_raw.strip():
                error = "Please provide resume text or upload a PDF."
            elif not jd_raw.strip():
                error = "Please provide a job description."

            if not error:
                resume_clean = normalize_text(resume_raw)
                jd_clean = normalize_text(jd_raw)
                catalog = _load_skills_catalog()
                analysis = analyze_resume(resume_clean, jd_clean, catalog)
                result = score(analysis)
        except Exception as e:
            error = f"Error processing input: {e}"

    return render_template("index.html", result=result, error=error)


@app.route("/api/v1/analyze", methods=["POST"])
def api_analyze():
    """REST API endpoint for headless integrations."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    resume_text = data.get("resume_text", "")
    jd_text = data.get("job_description", "")

    if not resume_text.strip():
        return jsonify({"error": "Missing resume_text"}), 400
    if not jd_text.strip():
        return jsonify({"error": "Missing job_description"}), 400

    try:
        resume_clean = normalize_text(resume_text)
        jd_clean = normalize_text(jd_text)
        catalog = _load_skills_catalog()
        analysis = analyze_resume(resume_clean, jd_clean, catalog)
        result = score(analysis)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
