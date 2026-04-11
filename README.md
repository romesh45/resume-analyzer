# Aura ATS — Intelligent Resume Analyzer

A lightweight ATS (Applicant Tracking System) that scores resumes against job descriptions using rule-based NLP. Built with Flask, pure Python, and zero ML dependencies.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

<!-- Add a screenshot after deployment -->
<!-- ![Aura ATS Demo](docs/screenshot.png) -->

---

## Features

- **Resume ↔ JD Matching** — Extracts skills from both inputs and computes overlap
- **PDF Upload** — Parses uploaded PDF resumes via PyPDF2 (no OCR)
- **Weighted Scoring** — Match percentage with tiered feedback (Strong / Moderate / Poor fit)
- **Skill Gap Analysis** — Clearly shows matched and missing skills
- **Client + Server Validation** — Prevents empty submissions on both layers
- **Production-Ready** — Gunicorn support, absolute paths, defensive error handling

---

## How It Works

```
Resume (PDF or text)  ──┐
                        ├──→  Normalize  ──→  Extract Skills  ──→  Compare  ──→  Score + Feedback
Job Description (text) ─┘
```

1. **Preprocess** — Lowercases text, strips punctuation, normalizes whitespace
2. **Analyze** — Scans both texts against a skills catalog (`data/skills.json`) and identifies matches
3. **Score** — Calculates `(matched / total_jd_skills) × 100` and generates actionable feedback
4. **Render** — Displays results with color-coded score, skill pills, and gap analysis

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9+, Flask |
| PDF Parsing | PyPDF2 |
| Text Processing | `re` (regex), custom tokenizer |
| Frontend | HTML5, CSS3, Vanilla JS |
| Templating | Jinja2 |
| Production Server | Gunicorn |

---

## Project Structure

```
aura-ats/
├── src/
│   ├── __init__.py
│   ├── app.py            # Flask routes and request handling
│   ├── preprocess.py     # Text extraction (PDF/text) and normalization
│   ├── analyzer.py       # Skill extraction and resume-JD comparison
│   └── scorer.py         # Scoring engine and feedback generation
├── templates/
│   └── index.html        # UI with form, validation, and results display
├── data/
│   └── skills.json       # Skills catalog (categories + keywords)
├── tests/
│   └── test_scorer.py    # Unit tests for analyzer and scorer
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# Clone
git clone https://github.com/your-username/aura-ats.git
cd aura-ats

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m flask --app src.app run --port 5000
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Run Tests

```bash
python -m unittest tests.test_scorer -v
```

---

## Deploy to Render

1. Push this repo to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your repository
4. Configure:

| Setting | Value |
|---------|-------|
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn src.app:app` |

5. Deploy

---

## Future Improvements

- [ ] Semantic matching using word embeddings (spaCy / sentence-transformers)
- [ ] Multi-format upload support (DOCX, TXT)
- [ ] Batch resume processing for recruiter workflows
- [ ] Persistent history with SQLite
- [ ] Exportable PDF report

---

## Author

**Romesh** — [GitHub](https://github.com/your-username)

---

## License

MIT
