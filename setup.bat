@echo off
REM AI Personality System - One-Click Setup
echo.
echo ================================================================
echo   AI Personality & Career System - Setup
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not installed!
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python installed: 
python --version

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed

REM Download NLTK data
echo.
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo OK: NLTK data downloaded

REM Check MongoDB connection
echo.
echo ================================================================
echo   MongoDB Setup
echo ================================================================
echo.
python -c "from database.connection import get_db; db = get_db(); print('OK: MongoDB connected')"
if errorlevel 1 (
    echo.
    echo ERROR: Could not connect to MongoDB!
    echo.
    echo Please ensure MongoDB is running:
    echo   1. Open a new terminal
    echo   2. Run: mongod
    echo   3. Then run this setup again
    echo.
    echo Download MongoDB: https://www.mongodb.com/try/download/community
    echo.
    pause
    exit /b 1
)

REM Ask about resetting database
echo.
echo ================================================================
echo   Database Setup
echo ================================================================
echo.
set /p RESET=Reset database? This will clear all existing data (y/n): 
if /i "%RESET%"=="y" (
    echo.
    echo Resetting database...
    python -c "
from database.connection import get_db
db = get_db()
db.users.delete_many({})
db.personalities.delete_many({})
db.questions.delete_many({})
db.careers.delete_many({})
db.recommendations.delete_many({})
db.quiz_history.delete_many({})
print('Database cleared')
"
    echo OK: Database cleared
)

REM Seed database
echo.
echo Seeding database with initial data...
python -c "from database.seed import seed_all; seed_all()"
if errorlevel 1 (
    echo WARNING: Could not seed database
) else (
    echo.
    echo OK: Database seeded successfully
)

echo.
echo ================================================================
echo   Setup Complete!
echo ================================================================
echo.
echo Next step: Run START.bat to launch the application
echo.
pause
