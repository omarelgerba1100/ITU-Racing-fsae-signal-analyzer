@echo off
echo Starting Advanced Engineering Analysis Tool...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python main.py
) else (
    python main.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start.
    echo Please run install_windows.bat first.
    pause
)
