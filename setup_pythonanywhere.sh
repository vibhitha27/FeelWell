#!/bin/bash
# Setup script for PythonAnywhere deployment

echo "Setting up FeelWell Mental Health Application..."

# Create virtual environment
echo "Creating virtual environment..."
mkvirtualenv --python=python3.9 feelwell-env
workon feelwell-env

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables prompt
echo "========================================"
echo "IMPORTANT: You need to set up your Groq API key."
echo "Run the following command (replace with your actual API key):"
echo "echo \"export GROQ_API_KEY='your_actual_groq_api_key'\" >> ~/.virtualenvs/feelwell-env/bin/postactivate"
echo "Then run: workon feelwell-env"
echo "========================================"

echo "Setup complete! Now configure your web app in the PythonAnywhere Web tab."
echo "Don't forget to edit the WSGI file as mentioned in the README."