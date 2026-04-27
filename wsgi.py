"""WSGI entry point for production deployment."""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from src.app import app

if __name__ == "__main__":
    app.run()
