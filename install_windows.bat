@echo off
echo ============================================
echo  Advanced Engineering Analysis Tool
echo  ITU Racing Team - Installation Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python found.
echo.

REM Create virtual environment (optional but recommended)
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [WARNING] Could not create virtual environment.
    echo Installing packages globally...
    goto install_global
)

echo [OK] Virtual environment created.
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

:install_packages
echo Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install some packages.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Installation Complete!
echo ============================================
echo.
echo To run the application:
echo   1. Double-click run_app.bat
echo   OR
echo   2. Open terminal and run: python main.py
echo.
pause
exit /b 0

:install_global
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install some packages.
    pause
    exit /b 1
)
echo.
echo ============================================
echo  Installation Complete!
echo ============================================
echo.
echo To run the application, run: python main.py
echo.
pause
exit /b 0
