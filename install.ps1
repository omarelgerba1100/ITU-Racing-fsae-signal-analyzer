#Requires -Version 5.1
<#
.SYNOPSIS
    ITU Racing - FSAE Signal Analysis Tool Installer

.DESCRIPTION
    Automated installer for the FSAE Signal Analysis Tool.
    Creates virtual environment, installs dependencies, and sets up shortcuts.

.EXAMPLE
    .\install.ps1

.NOTES
    Run in PowerShell as Administrator for best results.
    If you get execution policy errors, run:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#>

# Colors for output
$Host.UI.RawUI.WindowTitle = "ITU Racing - FSAE Tool Installer"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    Clear-Host
    Write-ColorOutput @"

+======================================================================+
|                                                                      |
|     ██╗████████╗██╗   ██╗    ██████╗  █████╗  ██████╗██╗███╗   ██╗   |
|     ██║╚══██╔══╝██║   ██║    ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║   |
|     ██║   ██║   ██║   ██║    ██████╔╝███████║██║     ██║██╔██╗ ██║   |
|     ██║   ██║   ██║   ██║    ██╔══██╗██╔══██║██║     ██║██║╚██╗██║   |
|     ██║   ██║   ╚██████╔╝    ██║  ██║██║  ██║╚██████╗██║██║ ╚████║   |
|     ╚═╝   ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═══╝   |
|                                                                      |
|              FSAE Signal Analysis Tool - Installer                   |
|                                                                      |
+======================================================================+

"@ -Color Cyan
}

function Test-PythonInstalled {
    Write-ColorOutput "`n[1/5] Checking Python installation..." -Color Yellow

    $pythonCommands = @("python", "python3", "py")

    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>&1
            if ($version -match "Python (\d+)\.(\d+)") {
                $major = [int]$Matches[1]
                $minor = [int]$Matches[2]

                if ($major -ge 3 -and $minor -ge 8) {
                    Write-ColorOutput "       Found: $version" -Color Green
                    return $cmd
                } else {
                    Write-ColorOutput "       Found $version but need Python 3.8+" -Color Red
                }
            }
        } catch {
            continue
        }
    }

    return $null
}

function New-VirtualEnvironment {
    param([string]$PythonCmd)

    Write-ColorOutput "`n[2/5] Creating virtual environment..." -Color Yellow

    if (Test-Path ".\venv") {
        Write-ColorOutput "       Virtual environment already exists" -Color Cyan
        $response = Read-Host "       Recreate it? (y/N)"
        if ($response -eq "y" -or $response -eq "Y") {
            Remove-Item -Recurse -Force ".\venv"
        } else {
            Write-ColorOutput "       Using existing virtual environment" -Color Green
            return $true
        }
    }

    try {
        & $PythonCmd -m venv venv
        Write-ColorOutput "       Virtual environment created successfully" -Color Green
        return $true
    } catch {
        Write-ColorOutput "       Failed to create virtual environment: $_" -Color Red
        return $false
    }
}

function Install-Dependencies {
    Write-ColorOutput "`n[3/5] Installing dependencies..." -Color Yellow
    Write-ColorOutput "       This may take a few minutes..." -Color Gray

    # Activate virtual environment
    $activateScript = ".\venv\Scripts\Activate.ps1"

    if (-not (Test-Path $activateScript)) {
        Write-ColorOutput "       Virtual environment activation script not found" -Color Red
        return $false
    }

    try {
        # Run pip install in the virtual environment
        & .\venv\Scripts\python.exe -m pip install --upgrade pip -q
        Write-ColorOutput "       Upgraded pip" -Color Gray

        & .\venv\Scripts\pip.exe install -r requirements.txt

        Write-ColorOutput "       All dependencies installed successfully" -Color Green
        return $true
    } catch {
        Write-ColorOutput "       Failed to install dependencies: $_" -Color Red
        return $false
    }
}

function Test-Installation {
    Write-ColorOutput "`n[4/5] Verifying installation..." -Color Yellow

    $requiredModules = @(
        "customtkinter",
        "CTkMessagebox",
        "plotly",
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "PIL"
    )

    $allGood = $true

    foreach ($module in $requiredModules) {
        $checkModule = $module
        if ($module -eq "PIL") { $checkModule = "PIL" }

        $result = & .\venv\Scripts\python.exe -c "import $checkModule" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "       [OK] $module" -Color Green
        } else {
            Write-ColorOutput "       [FAIL] $module" -Color Red
            $allGood = $false
        }
    }

    return $allGood
}

function New-RunScript {
    Write-ColorOutput "`n[5/5] Creating run scripts..." -Color Yellow

    # Create batch file for easy running
    $batchContent = @"
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python run_analyzer.py
pause
"@

    Set-Content -Path ".\Run_FSAE_Tool.bat" -Value $batchContent
    Write-ColorOutput "       Created Run_FSAE_Tool.bat" -Color Green

    # Create PowerShell run script
    $psContent = @"
# ITU Racing - FSAE Signal Analysis Tool
# Quick run script

Set-Location `$PSScriptRoot
& .\venv\Scripts\Activate.ps1
python run_analyzer.py
"@

    Set-Content -Path ".\Run_FSAE_Tool.ps1" -Value $psContent
    Write-ColorOutput "       Created Run_FSAE_Tool.ps1" -Color Green

    return $true
}

function Show-Completion {
    param([bool]$Success)

    Write-Host ""
    Write-Host ""

    if ($Success) {
        Write-ColorOutput @"
+======================================================================+
|                    INSTALLATION COMPLETE!                            |
+======================================================================+

  To run the application:

    Option 1: Double-click 'Run_FSAE_Tool.bat'

    Option 2: In PowerShell:
              .\venv\Scripts\Activate.ps1
              python run_analyzer.py

    Option 3: Run directly:
              .\venv\Scripts\python.exe run_analyzer.py

+======================================================================+
|                      ITU Racing Electronics                          |
+======================================================================+

"@ -Color Green
    } else {
        Write-ColorOutput @"
+======================================================================+
|                    INSTALLATION FAILED                               |
+======================================================================+

  Please check the errors above and try again.

  Common fixes:
    1. Make sure Python 3.8+ is installed and in PATH
    2. Run PowerShell as Administrator
    3. Check your internet connection
    4. Try: pip install --user -r requirements.txt

  For help, contact the electronics team or open a GitHub issue.

+======================================================================+

"@ -Color Red
    }
}

# Main installation flow
Write-Header

$pythonCmd = Test-PythonInstalled

if (-not $pythonCmd) {
    Write-ColorOutput "`n[ERROR] Python 3.8+ is required but not found!" -Color Red
    Write-ColorOutput "        Download from: https://www.python.org/downloads/" -Color Yellow
    Write-ColorOutput "        Make sure to check 'Add Python to PATH' during installation" -Color Yellow
    Show-Completion -Success $false
    Read-Host "`nPress Enter to exit"
    exit 1
}

$venvOk = New-VirtualEnvironment -PythonCmd $pythonCmd
if (-not $venvOk) {
    Show-Completion -Success $false
    Read-Host "`nPress Enter to exit"
    exit 1
}

$depsOk = Install-Dependencies
if (-not $depsOk) {
    Show-Completion -Success $false
    Read-Host "`nPress Enter to exit"
    exit 1
}

$verifyOk = Test-Installation
if (-not $verifyOk) {
    Write-ColorOutput "`n[WARNING] Some modules failed to import, but installation may still work" -Color Yellow
}

New-RunScript | Out-Null

Show-Completion -Success $true

$runNow = Read-Host "Run the application now? (Y/n)"
if ($runNow -ne "n" -and $runNow -ne "N") {
    Write-ColorOutput "`nStarting FSAE Signal Analysis Tool..." -Color Cyan
    & .\venv\Scripts\python.exe run_analyzer.py
}
