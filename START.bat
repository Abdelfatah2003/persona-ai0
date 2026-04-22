@echo off
setlocal

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo ================================================================
echo   AI Personality Quiz - Starting
echo ================================================================
echo.

echo [1/4] Checking venv...
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Run setup.bat first!
    pause
    exit /b 1
)
echo OK: venv found

echo.
echo [2/4] Checking packages...
"venv\Scripts\python.exe" -c "import flask; print('Flask OK')" 2>nul
if errorlevel 1 (
    "venv\Scripts\pip.exe" install -r requirements.txt
)
echo OK: Packages ready

echo.
echo [3/4] Connecting to MongoDB...
"venv\Scripts\python.exe" -c "from dotenv import load_dotenv; load_dotenv(); from database.connection import get_client; get_client().admin.command('ping'); print('MongoDB OK')" 2>nul
if errorlevel 1 (
    echo ERROR: Cannot connect to MongoDB
    echo.
    echo Check:
    echo   1. Atlas - Network Access: add 0.0.0.0/0
    echo   2. Atlas - User: abodzxsh777_db_user
    echo   3. Atlas - Password: Abod123456
    pause
    exit /b 1
)

echo.
echo [4/4] Starting Flask server...
start "AI Personality Server" cmd /k "cd /d %PROJECT_DIR% && venv\Scripts\python.exe app.py"

timeout /t 3 /nobreak >nul

echo.
echo Server starting at http://localhost:5000
start http://localhost:5000/

echo ================================================================
echo   Ready! Open http://localhost:5000 in browser
echo ================================================================
pause