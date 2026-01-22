@echo off
setlocal EnableDelayedExpansion

title FSAE Signal Analyzer - Quick Installer
color 0B

echo.
echo ============================================================
echo   FSAE Signal Analyzer - Quick Installer
echo   ITU Racing Electronics
echo ============================================================
echo.

:: Check if running as admin (needed for Program Files installation)
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Not running as administrator.
    echo     For Program Files installation, please run as Administrator.
    echo     Proceeding with user-level installation...
    echo.
    set "INSTALL_DIR=%LOCALAPPDATA%\FSAE Signal Analyzer"
) else (
    set "INSTALL_DIR=%ProgramFiles%\FSAE Signal Analyzer"
)

:: Check if the exe exists
set "EXE_SOURCE=dist\FSAE_Signal_Analyzer.exe"
if not exist "%EXE_SOURCE%" (
    set "EXE_SOURCE=FSAE_Signal_Analyzer.exe"
)
if not exist "%EXE_SOURCE%" (
    echo [ERROR] Cannot find FSAE_Signal_Analyzer.exe
    echo         Please ensure you're running this from the correct directory.
    echo.
    echo         Expected locations:
    echo         - dist\FSAE_Signal_Analyzer.exe
    echo         - FSAE_Signal_Analyzer.exe
    echo.
    pause
    exit /b 1
)

echo Found executable: %EXE_SOURCE%
echo.
echo Installation Options:
echo.
echo   1. Install to: %INSTALL_DIR%
echo   2. Choose custom location
echo   3. Cancel
echo.

set /p CHOICE="Select option (1/2/3) [default: 1]: "
if "%CHOICE%"=="" set CHOICE=1

if "%CHOICE%"=="3" (
    echo Installation cancelled.
    pause
    exit /b 0
)

if "%CHOICE%"=="2" (
    set /p INSTALL_DIR="Enter installation path: "
)

:: Validate installation directory
if "%INSTALL_DIR%"=="" (
    echo [ERROR] Invalid installation path.
    pause
    exit /b 1
)

echo.
echo [*] Installing to: %INSTALL_DIR%
echo.

:: Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%" 2>nul
    if errorlevel 1 (
        echo [ERROR] Failed to create directory: %INSTALL_DIR%
        echo         Try running as Administrator or choose a different location.
        pause
        exit /b 1
    )
)

:: Copy the executable
echo [*] Copying executable...
copy /Y "%EXE_SOURCE%" "%INSTALL_DIR%\FSAE_Signal_Analyzer.exe" >nul
if errorlevel 1 (
    echo [ERROR] Failed to copy executable.
    pause
    exit /b 1
)
echo [OK] Executable installed.

:: Copy icon if available
if exist "assets\icon.ico" (
    if not exist "%INSTALL_DIR%\assets" mkdir "%INSTALL_DIR%\assets" 2>nul
    copy /Y "assets\icon.ico" "%INSTALL_DIR%\assets\icon.ico" >nul 2>nul
)

:: Create shortcuts using PowerShell
echo [*] Creating shortcuts...

:: Desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_DESKTOP=%DESKTOP%\FSAE Signal Analyzer.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
    $s = $ws.CreateShortcut('%SHORTCUT_DESKTOP%'); ^
    $s.TargetPath = '%INSTALL_DIR%\FSAE_Signal_Analyzer.exe'; ^
    $s.WorkingDirectory = '%INSTALL_DIR%'; ^
    $s.Description = 'FSAE Signal Analyzer - ITU Racing'; ^
    if (Test-Path '%INSTALL_DIR%\assets\icon.ico') { $s.IconLocation = '%INSTALL_DIR%\assets\icon.ico' }; ^
    $s.Save()"

if exist "%SHORTCUT_DESKTOP%" (
    echo [OK] Desktop shortcut created.
) else (
    echo [!] Failed to create desktop shortcut.
)

:: Start Menu shortcut
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "STARTMENU_FOLDER=%STARTMENU%\ITU Racing"

if not exist "%STARTMENU_FOLDER%" mkdir "%STARTMENU_FOLDER%" 2>nul

set "SHORTCUT_START=%STARTMENU_FOLDER%\FSAE Signal Analyzer.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
    $s = $ws.CreateShortcut('%SHORTCUT_START%'); ^
    $s.TargetPath = '%INSTALL_DIR%\FSAE_Signal_Analyzer.exe'; ^
    $s.WorkingDirectory = '%INSTALL_DIR%'; ^
    $s.Description = 'FSAE Signal Analyzer - ITU Racing'; ^
    if (Test-Path '%INSTALL_DIR%\assets\icon.ico') { $s.IconLocation = '%INSTALL_DIR%\assets\icon.ico' }; ^
    $s.Save()"

if exist "%SHORTCUT_START%" (
    echo [OK] Start Menu shortcut created.
) else (
    echo [!] Failed to create Start Menu shortcut.
)

:: Create uninstaller batch file
set "UNINSTALLER=%INSTALL_DIR%\uninstall.bat"
(
echo @echo off
echo title FSAE Signal Analyzer - Uninstaller
echo echo.
echo echo ============================================================
echo echo   FSAE Signal Analyzer - Uninstaller
echo echo ============================================================
echo echo.
echo set /p CONFIRM="Are you sure you want to uninstall? (Y/N): "
echo if /i "%%CONFIRM%%"=="Y" ^(
echo     echo [*] Removing application files...
echo     del /q "%INSTALL_DIR%\FSAE_Signal_Analyzer.exe" 2^>nul
echo     rmdir /s /q "%INSTALL_DIR%\assets" 2^>nul
echo     echo [*] Removing shortcuts...
echo     del /q "%SHORTCUT_DESKTOP%" 2^>nul
echo     del /q "%SHORTCUT_START%" 2^>nul
echo     rmdir "%STARTMENU_FOLDER%" 2^>nul
echo     echo [OK] Uninstallation complete.
echo     echo [*] Removing installation folder...
echo     cd /d "%%TEMP%%"
echo     rmdir /s /q "%INSTALL_DIR%" 2^>nul
echo ^) else ^(
echo     echo Uninstallation cancelled.
echo ^)
echo pause
) > "%UNINSTALLER%"

echo [OK] Uninstaller created.

echo.
echo ============================================================
echo   INSTALLATION COMPLETE!
echo ============================================================
echo.
echo   Application installed to:
echo   %INSTALL_DIR%
echo.
echo   Shortcuts created:
echo   - Desktop: %SHORTCUT_DESKTOP%
echo   - Start Menu: %STARTMENU_FOLDER%
echo.
echo   To uninstall, run:
echo   %UNINSTALLER%
echo.
echo ============================================================
echo.

set /p LAUNCH="Launch FSAE Signal Analyzer now? (Y/N) [default: Y]: "
if "%LAUNCH%"=="" set LAUNCH=Y

if /i "%LAUNCH%"=="Y" (
    echo [*] Launching application...
    start "" "%INSTALL_DIR%\FSAE_Signal_Analyzer.exe"
)

echo.
echo Installation finished. Press any key to exit...
pause >nul
