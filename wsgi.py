"""WSGI entry point for production deployment."""
import os
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Ensure required directories exist
base_dir = Path(__file__).resolve().parent
(base_dir / "uploads").mkdir(exist_ok=True)

from src.app import app

if __name__ == "__main__":
    app.run()
