# Aura ATS — AI Resume Analyzer

> **Upload a resume. Paste a job description. Get an instant ATS-style match score with skill gap analysis.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Tests](https://img.shields.io/badge/Tests-12%20passing-brightgreen)](tests/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render%20Ready-46E3B7?logo=render&logoColor=white)](https://render.com)

---

## What It Does

- Extracts skills from a resume (PDF upload or plain text) and a job description
- Computes an ATS-style match score from 0–100
- Returns matched skills and missing skills as a structured report
- Exposes both a web UI and a REST API endpoint

---

## Features

- **Resume ↔ JD Matching** — Skill extraction from both inputs, overlap computed as a percentage score
- **PDF Upload** — Parses text-based PDFs via PyPDF2; falls back gracefully on extraction failures
- **Skill Gap Report** — Matched skills (green) and missing skills (red) rendered as visual pills
- **Tiered Scoring Engine** — 0–100 score with categorical feedback: Strong / Moderate / Poor fit
- **REST API** — Headless JSON endpoint at `/api/v1/analyze` for external integrations
- **Dual-Layer Validation** — Client-side JS + server-side Flask; the app never crashes on bad input
- **Deploy-Ready** — Gunicorn-compatible with production-safe path resolution out of the box

---

## How to Use

1. **Paste or upload** your resume — plain text or a text-based PDF
2. **Paste** the target job description
3. **Click** Analyze Fit
4. **Review** your match score, matched skills, and the gaps to address

---

## Demo

**Input — Upload resume + paste job description**

![Aura ATS Input UI](<img width="1710" height="1112" alt="Screenshot 2026-04-11 at 8 52 41 PM" src="https://github.com/user-attachments/assets/c42d7887-9abc-4583-8c0a-e2e31abcc5c4" />
)

**Output — Match score: 80% with skill gap breakdown**

![Aura ATS Result 80](<img width="1710" height="1112" alt="Screenshot 2026-04-11 at 9 33 56 PM" src="https://github.com/user-attachments/assets/bab1a94e-cf00-4312-a196-504995a817a7" />
)

**Output — Perfect match: 100% with no gaps detected**

![Aura ATS Result 100](<img width="1710" height="1112" alt="Screenshot 2026-04-11 at 9 34 24 PM" src="https://github.com/user-attachments/assets/d1a965d9-0ea6-4f1e-bf9d-e5ae7a6c625c" />
)

---

## System Architecture

Four-stage pipeline with strict separation of concerns:

```
┌────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────────┐
│   Input    │───▶│  Preprocess  │───▶│   Analyze   │───▶│  Score & Render  │
│            │    │              │    │             │    │                  │
│ PDF / Text │    │ preprocess.py│    │ analyzer.py │    │    scorer.py     │
│ + JD text  │    │ Normalize,   │    │ Extract     │    │ Match %, Tiers,  │
│            │    │ PDF extract  │    │ skills from │    │ Feedback labels  │
└────────────┘    └──────────────┘    │ resume + JD │    └──────────────────┘
                                      └─────────────┘
                                            │
                                     skills.json catalog
                                     (extensible keyword map)
```

| Stage | Module | Responsibility |
|-------|--------|----------------|
| Extract | `preprocess.py` | PDF stream parsing, text normalization, encoding handling |
| Analyze | `analyzer.py` | Skill extraction against catalog, set intersection |
| Score | `scorer.py` | Match % calculation, score bucketing, feedback generation |
| Serve | `app.py` | Flask routing, file validation, HTML + JSON response dispatch |

---

## Engineering Highlights

**Modular pipeline** — Each stage is independently testable and swappable. `scorer.py` has no knowledge of Flask; `analyzer.py` has no knowledge of file I/O. Clean boundaries mean swapping the keyword matcher for a transformer model is a single-module change with zero ripple.

**Defensive file handling** — `file.seek(0)` resets the stream before PyPDF2 reads it; `None` guards prevent silent failures when extraction returns empty. The app degrades gracefully rather than crashing.

**Production-safe paths** — All data file references use `_BASE_DIR` anchored to the module's `__file__`, ensuring `skills.json` resolves correctly whether launched via `flask run`, `gunicorn`, or any working directory.

**Zero heavy ML dependencies** — Skill extraction uses a regex + keyword catalog approach. No spaCy, no model download, no GPU required. Cold start is under 1 second.

**12 unit tests** — Edge-case coverage across `scorer.py`: empty inputs, partial matches, exact matches, zero overlap, and boundary score values. Runs with a single command, no mocking required.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9+, Flask 3.x |
| PDF Parsing | PyPDF2 |
| NLP / Matching | Regex + extensible keyword catalog (`skills.json`) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Templating | Jinja2 |
| Production Server | Gunicorn |

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

## Deployment (Render)

| Setting | Value |
|---------|-------|
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn src.app:app` |

`_BASE_DIR`-based path resolution ensures `skills.json` loads correctly under Gunicorn's working directory — no extra configuration needed.

---

## REST API

The `/api/v1/analyze` endpoint accepts JSON and returns a structured match report:

```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Python SQL developer", "job_description": "Python SQL JavaScript"}'
```

**Response:**

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

## Project Structure

```
resume-analyzer/
├── src/
│   ├── app.py            # Flask routes — web UI + REST API
│   ├── preprocess.py     # PDF extraction + text normalization
│   ├── analyzer.py       # Skill extraction + JD comparison logic
│   └── scorer.py         # Scoring engine + tiered feedback
├── templates/
│   └── index.html        # UI: upload form, client validation, results render
├── data/
│   └── skills.json       # Extensible skills catalog
├── tests/
│   └── test_scorer.py    # 12 unit tests (edge cases + boundary values)
├── docs/                 # Screenshots for README
├── uploads/              # Ephemeral file store (gitignored)
├── requirements.txt
└── README.md
```

---

## Future Improvements

- **Semantic matching** — Sentence-transformers for synonym-aware comparison (e.g., "ML" ↔ "machine learning")
- **Multi-format uploads** — DOCX and TXT support alongside PDF
- **Batch processing** — Multi-resume ranking against a single JD
- **Persistence layer** — SQLite-backed history for tracking score trends over time

---

## Author

**Romesh** — Final-year IT Engineer | AI/ML Enthusiast

[github.com/romesh45](https://github.com/romesh45)

---

*Built with Python and Flask. MIT Licensed.*
