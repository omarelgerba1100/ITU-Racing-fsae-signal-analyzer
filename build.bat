@echo off
title ITU Racing - FSAE Signal Analyzer Build Tool
color 0A

echo.
echo ============================================================
echo   ITU Racing - FSAE Signal Analyzer Build Tool
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo         Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

:: Run the build script with option 3 (build exe + create installer script)
echo Starting build process...
echo.
python build_exe.py 3

echo.
echo ============================================================
echo   Build Complete!
echo ============================================================
echo.
echo   Your files are ready:
echo   - Standalone EXE: dist\FSAE_Signal_Analyzer.exe
echo   - Installer Script: installer_script.iss
echo.
echo   To create a professional installer:
echo   1. Install InnoSetup from https://jrsoftware.org/isinfo.php
echo   2. Open installer_script.iss with InnoSetup
echo   3. Click Build ^> Compile
echo.
pause
