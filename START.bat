@echo off
echo ================================================================
echo   AI Personality Quiz - Starting
echo ================================================================
echo.

echo Checking Flask...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ERROR: Flask not installed. Run setup.bat first.
    pause
    exit /b 1
)
echo OK: Flask ready

echo.
echo Checking MongoDB...
python -c "from database.connection import get_db; get_db()" 2>nul
if errorlevel 1 (
    echo ERROR: Cannot connect to MongoDB. Make sure MongoDB is running.
    echo.
    echo If MongoDB is not running, open a new terminal and run:
    echo   mongod
    echo.
    pause
    exit /b 1
)
echo OK: MongoDB connected

echo.
echo ================================================================
echo   Starting Server
echo ================================================================
echo.

start "AI Backend" cmd /k "cd /d %~dp0 && python app.py"

echo Waiting for server...
timeout /t 4 /nobreak >nul

curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: Server may not have started. Check AI Backend window.
) else (
    echo OK: Server is running at http://localhost:5000
    start http://localhost:5000/
)

echo.
echo ================================================================
echo   Ready!
echo ================================================================
echo   Server: http://localhost:5000
echo   Debug API: http://localhost:5000/api/recommendations/debug
echo.
echo   Close the AI Backend window to stop the server.
echo.
pause
