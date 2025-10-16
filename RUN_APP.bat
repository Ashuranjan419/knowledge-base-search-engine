@echo off
cls
echo ========================================
echo   KNOWLEDGE BASE SEARCH ENGINE
echo   Complete System Startup
echo ========================================
echo.

REM Kill any existing Python processes
echo [1/4] Stopping existing processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start Backend
echo [2/4] Starting Backend Server (Port 8000)...
cd /d "%~dp0backend"
start "Backend Server" cmd /c "call ..\.venv\Scripts\activate.bat && python main.py"
cd..

REM Wait for backend to start
echo [3/4] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [4/4] Starting Frontend Server (Port 3000)...
start "Frontend Server" cmd /c "call .venv\Scripts\activate.bat && python start_frontend.py"

REM Wait and open browser
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend App: http://localhost:3000
echo.
echo ========================================
echo.
echo Opening browser...
start http://localhost:3000

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
