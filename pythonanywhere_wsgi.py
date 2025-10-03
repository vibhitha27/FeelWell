"""
This is a WSGI configuration file for PythonAnywhere.
Replace 'yourusername' with your actual PythonAnywhere username.
"""

import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/FeelWell'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['GROQ_API_KEY'] = 'your_actual_groq_api_key'

# Import your Flask app
from app import app as application