@echo off
echo ========================================
echo  Knowledge Base Search Engine
echo ========================================
echo.
echo Starting server...
echo.
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: Open frontend/index.html in browser
echo.
echo Press CTRL+C to stop the server
echo.

cd /d "%~dp0backend"
call ..\.venv\Scripts\activate.bat
python main.py
pause
