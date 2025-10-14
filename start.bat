@echo off
REM Knowledge Base Search Engine - Windows Startup Script

echo Starting Knowledge Base Search Engine...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
cd backend
pip install -r requirements.txt

REM Check if .env exists
if not exist "..\\.env" (
    echo Warning: .env file not found!
    echo Creating .env from .env.example...
    copy "..\.env.example" "..\.env"
    echo Please edit .env file with your API keys before running.
    pause
    exit /b 1
)

REM Start the server
echo Starting FastAPI server...
python main.py
