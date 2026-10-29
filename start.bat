@echo off
TITLE Workmate — Start All Services

echo.
echo  ==========================================
echo   Workmate — AI Productivity Hub
echo   Starting Backend + Frontend ...
echo  ==========================================
echo.

:: --- Start Backend (FastAPI) ---
echo [1/2] Starting Backend on http://localhost:8000 ...
start "Workmate Backend (FastAPI)" cmd /k "cd /d d:\PA\Workmate\backend && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

:: --- Start Frontend (Python HTTP server) ---
echo [2/2] Starting Frontend on http://localhost:3000 ...
start "Workmate Frontend (HTTP Server)" cmd /k "py -m http.server 3000 --directory d:\PA\Workmate\frontend"

:: Wait 2 seconds, then open browser
timeout /t 2 /nobreak >nul

echo.
echo  ==========================================
echo   ✅  All services started!
echo   Frontend : http://localhost:3000
echo   Backend  : http://localhost:8000
echo   API Docs : http://localhost:8000/api/docs
echo  ==========================================
echo.

:: Open browser
start http://localhost:3000

pause
