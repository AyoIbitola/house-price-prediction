import sys
import os

# Add the project root to the python path to import app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as application
