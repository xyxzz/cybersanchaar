#!/usr/bin/env python3
"""
WSGI entry point for Gunicorn
This file creates the Flask application instance for production deployment
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.config import Config
from src.web_interface import create_app

# Create the Flask application
config = Config()
app = create_app(config)

if app is None:
    raise RuntimeError("Failed to create Flask application. Make sure Flask is installed.")

if __name__ == "__main__":
    # This will only run if you execute wsgi.py directly (for testing)
    print("Running Flask app in development mode...")
    app.run(host='0.0.0.0', port=5000, debug=False)

