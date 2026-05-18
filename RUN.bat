@echo off
cd /d "%~dp0"

call .venv\Scripts\activate
python -m bongo_cat

echo.
pause
