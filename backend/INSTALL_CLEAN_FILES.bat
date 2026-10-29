@echo off
echo ================================================
echo   COSMIC ASSISTANT - CLEAN FILES INSTALLATION
echo ================================================
echo.

echo [1/3] Backing up old files...
if exist app\routes\*.py (
    mkdir backup_corrupted 2>nul
    xcopy app\routes\*.py backup_corrupted\ /Y >nul
    echo ✓ Old files backed up to backup_corrupted\
)

echo.
echo [2/3] Deleting corrupted files...
del app\routes\auth.py 2>nul
del app\routes\goals.py 2>nul
del app\routes\tasks.py 2>nul
del app\routes\notes.py 2>nul
del app\routes\ai_chat.py 2>nul
del app\routes\__init__.py 2>nul
del app\services\__init__.py 2>nul
del app\models\__init__.py 2>nul
del main.py 2>nul
echo ✓ Corrupted files deleted

echo.
echo [3/3] Ready to install clean files!
echo.
echo ================================================
echo   NEXT STEPS:
echo ================================================
echo.
echo 1. Copy ALL the clean files from the artifacts
echo 2. Save them in the correct locations
echo 3. Run: python main.py
echo.
echo Files to create:
echo   - main.py
echo   - app/routes/__init__.py
echo   - app/routes/auth.py
echo   - app/routes/goals.py
echo   - app/routes/tasks.py
echo   - app/routes/notes.py
echo   - app/routes/ai_chat.py
echo   - app/services/__init__.py
echo   - app/services/ai_service.py
echo   - app/models/__init__.py
echo.
pause