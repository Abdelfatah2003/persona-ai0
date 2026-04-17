@echo off
echo ================================================================
echo   Database Reset
echo ================================================================
echo.

echo This will DELETE all users and personalities.
set /p CONFIRM=Are you sure? (yes/no): 
if /i not "%CONFIRM%"=="yes" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Deleting personalities...
python -c "from database.connection import get_db; db=get_db(); r=db.personalities.delete_many({}); print(f'Deleted {r.deleted_count} personalities')"

echo Deleting users...
python -c "from database.connection import get_db; db=get_db(); r=db.users.delete_many({}); print(f'Deleted {r.deleted_count} users')"

echo.
echo Seeding fresh data...
python -c "from database.seed import seed_all; seed_all()"

echo.
echo ================================================================
echo   Reset Complete!
echo ================================================================
echo.
pause
