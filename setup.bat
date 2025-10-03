@echo off
REM This script sets up the environment for local development

echo Setting up the FeelWell mental health application for local development...

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit the .env file and add your actual API keys
) else (
    echo .env file already exists
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

echo Setup complete! You can now run the application with:
echo python app.py