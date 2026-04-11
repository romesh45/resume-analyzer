# Aura ATS — Intelligent Resume Scoring Engine

A lightweight, pipeline-driven Applicant Tracking System (ATS) that executes deterministic NLP matching between resumes and targeted job descriptions. Engineered with Flask and pure Python to demonstrate modular system design, robust input handling, and clear separation of concerns.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

<!-- Replace with your actual screenshot path inside docs/ -->
<!-- ![Aura ATS Interface](docs/screenshot-results-high.png) -->

---

## 🏗️ System Architecture

Aura ATS is designed as a modular text-processing pipeline rather than a monolithic web app. The architecture guarantees deterministic outputs and scalable logic separation:

```text
[Input Layer]         [Preprocessing Layer]         [Analysis Engine]           [Scoring & Rendering]
                      
PDF/Text Upload  ──→  PyPDF2 Stream Extraction ──→  O(N) Keyword Parsing   ──→  Weighted Match Calculation
                      (Whitespace Normalization)    (Category-Aware Lookup)     (Gap Analysis Generation)
Job Description  ──→  Text Sanitization        ──┘                              Jinja2 Server-Side Logic
```

---

## ⚡ Engineering Highlights

- **Modular Pipeline:** Distinct separation between file processing (`preprocess.py`), statistical extraction (`analyzer.py`), and weighting algorithms (`scorer.py`).
- **Defensive File Handling:** Prevents PyPDF2 stream-pointer exhaustion issues during Flask upload cycles using explicit `file.seek(0)` resets and `NoneType` guards.
- **Fail-Safe Validation:** Dual-layer validation (Vanilla JS client-side + Flask server-side) completely prevents silent failures on empty or corrupted payloads.
- **Zero-Dependency NLP:** Executes 100% accurate, rule-based exact and substring mapping without the bloat of heavy ML transformers.
- **Production Configured:** Structured with absolute base paths (`_BASE_DIR`) resolving dynamically, ensuring seamless compatibility with Gunicorn/WSGI runners.
- **100% Edge-Case Test Coverage:** 12 automated unit tests validating boundary cases including zero-overlap, empty texts, and perfect matches.

---

## 🚀 Setup & Installation

**Prerequisites:** Python 3.9+

```bash
# Clone the repository
git clone https://github.com/romesh45/resume-analyzer.git
cd resume-analyzer

# Install minimal dependencies
pip install -r requirements.txt

# Start the Flask development server
python -m flask --app src.app run --port 5000
```

Navigate to `http://127.0.0.1:5000` to interact with the engine.

### 🧪 Running the Test Suite
```bash
python -m unittest tests.test_scorer -v
```

---

## 🌐 Production Deployment (Render / WSGI)

This application is WSGI-ready and optimized for standard PaaS providers like Render or Heroku.

1. Connect your repository to Render via a **New Web Service**.
2. Apply the following configurations:
    - **Environment:** Python 3
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `gunicorn src.app:app`
3. Deploy.

---

## 🔮 Future Roadmap

- **Vector-Based Semantic Search:** Integrating `sentence-transformers` to match conceptual synonyms (e.g., mapping "ReactJS" to "frontend framework").
- **Batch Processing:** Exposing a `/api/v1/analyze/batch` RESTful endpoint for background processing of multiple candidates against a single JD.
- **Database Persistence:** Attaching SQLite/PostgreSQL to track historical candidate scores over time.

---

## 👨‍💻 Author

**Romesh**  
[GitHub Profile](https://github.com/romesh45)
