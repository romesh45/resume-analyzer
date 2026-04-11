"""Extract and normalize text from resume files (PDF, DOCX, plain text)."""

import re
from pathlib import Path

from PyPDF2 import PdfReader


def extract_text(file_obj) -> str:
    """
    Read a resume file and return raw text.
    Handles both string file paths and file-like objects (like Flask FileStorage).
    """
    if isinstance(file_obj, str):
        suffix = Path(file_obj).suffix.lower()
        if suffix == ".txt":
            return Path(file_obj).read_text(encoding="utf-8")
        if suffix == ".pdf":
            reader = PdfReader(file_obj)
            return "".join(page.extract_text() or "" for page in reader.pages)
        raise ValueError("Unsupported file type")
    else:
        # Handle file-like object (Flask FileStorage)
        filename = getattr(file_obj, "filename", "") or ""
        suffix = Path(filename).suffix.lower()

        # Reset stream pointer — Flask may have read headers already
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)

        if suffix == ".txt":
            return file_obj.read().decode("utf-8", errors="ignore")
        if suffix == ".pdf":
            reader = PdfReader(file_obj)
            return "".join(page.extract_text() or "" for page in reader.pages)
        raise ValueError(f"Unsupported file type: {suffix or 'unknown'}")


def normalize_text(text: str) -> str:
    """Lowercase, strip noise, and normalize whitespace."""
    text = text.lower()
    # keep word characters and spaces (Unicode-aware)
    text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
