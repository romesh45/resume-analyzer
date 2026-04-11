# Aura ATS — AI Resume Analyzer

Scores resumes against job descriptions using rule-based NLP. Upload a PDF or paste text, get an instant match score with skill gap analysis.

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
- **Skill Gap Analysis** — Shows matched skills (green) and missing skills (red) as visual pills
- **Tiered Scoring** — 0–100 score with feedback: Strong Fit / Moderate Fit / Poor Fit
- **Dual Validation** — Client-side JS + server-side Flask prevents all empty/invalid submissions
- **Deploy-Ready** — Works with Gunicorn out of the box

---

## How to Use

1. **Paste or upload** your resume (PDF or raw text)
2. **Paste** the target job description
3. **Click** "Analyze Fit"
4. **Review** your match score, matched skills, and missing skills

---

## Architecture

The system is built as a four-stage pipeline with strict separation of concerns:

```
Input  ──→  Preprocess  ──→  Analyze  ──→  Score & Render
```

| Stage | File | Responsibility |
|-------|------|---------------|
| **Extract** | `preprocess.py` | PDF text extraction, whitespace normalization |
| **Analyze** | `analyzer.py` | Skill matching against `skills.json` catalog |
| **Score** | `scorer.py` | Match percentage calculation, feedback generation |
| **Serve** | `app.py` | Flask routing, input validation, template rendering |

---

## Engineering Highlights

- **Modular pipeline** — Each stage is independently testable and replaceable
- **Defensive file handling** — `file.seek(0)` resets and `None` guards prevent PDF stream corruption
- **Dual-layer validation** — JS client-side + Flask server-side; the app never crashes on bad input
- **Zero heavy dependencies** — Pure Python NLP without spaCy or ML libraries
- **Absolute path resolution** — `_BASE_DIR` pattern ensures Gunicorn/WSGI compatibility
- **12 unit tests** — Full edge-case coverage: empty inputs, partial matches, perfect matches, zero overlap

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| PDF Parsing | PyPDF2 |
| NLP | Regex + custom keyword matcher |
| Frontend | HTML5, CSS3 (glassmorphism), Vanilla JS |
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
│   ├── app.py            # Flask routes + request handling
│   ├── preprocess.py     # PDF extraction + text normalization
│   ├── analyzer.py       # Skill extraction + JD comparison
│   └── scorer.py         # Scoring engine + feedback logic
├── templates/
│   └── index.html        # UI: form, validation, results display
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
- REST API endpoint (`/api/v1/analyze`) for headless integrations
- Multi-format support (DOCX, TXT)
- Historical tracking with SQLite

---

## Author

**Romesh** — [github.com/romesh45](https://github.com/romesh45)
