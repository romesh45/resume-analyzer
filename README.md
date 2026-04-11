# Aura ATS — AI Resume Analyzer

Scores resumes against job descriptions using NLP. Upload a PDF or paste text, get an instant match score with skill gap analysis.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-12%20passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

<!-- Uncomment after adding screenshots to docs/ -->
<!-- ![Aura ATS Demo](docs/screenshot-results.png) -->

---

## Features

- **Resume ↔ JD Matching** — Extracts skills from both inputs, computes overlap percentage
- **PDF Upload** — Parses uploaded resumes via PyPDF2 (text-based PDFs)
- **Skill Gap Analysis** — Matched skills (green) and missing skills (red) shown as visual pills
- **Tiered Scoring** — 0–100 score with feedback: Strong / Moderate / Poor fit
- **REST API** — JSON endpoint at `/api/v1/analyze` for headless integrations
- **Dual Validation** — Client-side JS + server-side Flask prevents all invalid submissions
- **Deploy-Ready** — Works with Gunicorn out of the box

---

## How to Use

1. **Paste or upload** your resume (PDF or raw text)
2. **Paste** the target job description
3. **Click** "Analyze Fit"
4. **Review** your match score, matched skills, and gaps

---

## Architecture

Four-stage pipeline with strict separation of concerns:

```
Input  ──→  Preprocess  ──→  Analyze  ──→  Score & Render
```

| Stage | File | What it does |
|-------|------|-------------|
| Extract | `preprocess.py` | PDF parsing, text normalization |
| Analyze | `analyzer.py` | Skill matching against `skills.json` catalog |
| Score | `scorer.py` | Match % calculation, feedback generation |
| Serve | `app.py` | Flask routing, validation, HTML + JSON responses |

---

## Engineering Highlights

- **Modular pipeline** — Each stage is independently testable and replaceable
- **Defensive file handling** — `file.seek(0)` resets and `None` guards prevent PDF stream issues
- **Dual-layer validation** — JS client + Flask server; the app never crashes on bad input
- **Zero heavy dependencies** — Pure Python NLP, no spaCy or ML libraries needed
- **Production paths** — `_BASE_DIR` pattern ensures Gunicorn/WSGI compatibility
- **12 unit tests** — Edge-case coverage: empty inputs, partial matches, full matches, zero overlap

---

## API

The app exposes a JSON endpoint alongside the web interface:

```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Python SQL developer", "job_description": "Python SQL JavaScript"}'
```

```json
{
  "status": "success",
  "data": {
    "overall_score": 67,
    "match_percentage": 66.67,
    "feedback": "Moderate fit — some relevant skills are present, but gaps remain.",
    "details": {
      "matched_skills": ["python", "sql"],
      "missing_skills": ["javascript"]
    }
  }
}
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| PDF Parsing | PyPDF2 |
| NLP | Regex + keyword matcher |
| Frontend | HTML5, CSS3, Vanilla JS |
| Templating | Jinja2 |
| Production | Gunicorn |

---

## Setup

```bash
git clone https://github.com/romesh45/resume-analyzer.git
cd resume-analyzer
pip install -r requirements.txt
python -m flask --app src.app run --port 5000
```

Open [http://localhost:5000](http://localhost:5000)

### Run Tests

```bash
python -m unittest tests.test_scorer -v
```

---

## Deploy to Render

| Setting | Value |
|---------|-------|
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn src.app:app` |

---

## Project Structure

```
resume-analyzer/
├── src/
│   ├── app.py            # Flask routes (web + API)
│   ├── preprocess.py     # PDF extraction + text normalization
│   ├── analyzer.py       # Skill extraction + JD comparison
│   └── scorer.py         # Scoring engine + feedback logic
├── templates/
│   └── index.html        # UI: form, validation, results
├── data/
│   └── skills.json       # Skills catalog (extensible)
├── tests/
│   └── test_scorer.py    # 12 unit tests
├── requirements.txt
└── README.md
```

---

## Future Improvements

- Semantic matching via sentence-transformers (synonym support)
- Multi-format uploads (DOCX, TXT)
- Batch candidate processing
- Historical tracking with SQLite

---

## Author

**Romesh** — [github.com/romesh45](https://github.com/romesh45)
