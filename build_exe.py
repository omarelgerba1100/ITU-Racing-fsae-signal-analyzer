#!/usr/bin/env python3
"""
ITU Racing - FSAE Signal Analysis Tool
Build Script for Standalone Executable

This script creates a standalone Windows executable using PyInstaller.
The resulting .exe can be distributed without requiring Python installation.

Usage:
    python build_exe.py

Requirements:
    pip install pyinstaller

Output:
    dist/FSAE_Signal_Analyzer.exe
"""

import subprocess
import sys
import os
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        return True

def build_executable():
    """Build the standalone executable."""

    print("\n" + "="*60)
    print("  ITU Racing - Building FSAE Signal Analyzer Executable")
    print("="*60 + "\n")

    # Check PyInstaller
    check_pyinstaller()

    # Clean previous builds
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            print(f"[*] Cleaning {folder}/...")
            shutil.rmtree(folder)

    # Remove old spec file
    spec_file = 'FSAE_Signal_Analyzer.spec'
    if os.path.exists(spec_file):
        os.remove(spec_file)

    print("\n[*] Building executable (this may take a few minutes)...\n")

    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=FSAE_Signal_Analyzer',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window (GUI app)
        '--clean',                      # Clean PyInstaller cache
        '--noconfirm',                  # Replace output without asking

        # Icon (if you have one, uncomment and add path)
        # '--icon=assets/icon.ico',

        # Hidden imports for customtkinter and other packages
        '--hidden-import=customtkinter',
        '--hidden-import=CTkMessagebox',
        '--hidden-import=plotly',
        '--hidden-import=plotly.express',
        '--hidden-import=plotly.graph_objects',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=scipy',
        '--hidden-import=scipy.signal',
        '--hidden-import=scipy.fft',
        '--hidden-import=matplotlib',
        '--hidden-import=matplotlib.pyplot',
        '--hidden-import=matplotlib.figure',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--hidden-import=openpyxl',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',

        # Collect all data for customtkinter (themes, etc.)
        '--collect-all=customtkinter',
        '--collect-all=CTkMessagebox',

        # Entry point
        'run_analyzer.py'
    ]

    try:
        subprocess.check_call(cmd)

        exe_path = os.path.join('dist', 'FSAE_Signal_Analyzer.exe')

        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print("\n" + "="*60)
            print("  BUILD SUCCESSFUL!")
            print("="*60)
            print(f"\n  Executable: {os.path.abspath(exe_path)}")
            print(f"  Size: {size_mb:.1f} MB")
            print("\n  You can now distribute this single .exe file!")
            print("  No Python installation required on target machines.")
            print("="*60 + "\n")
            return True
        else:
            print("\n[ERROR] Executable not found after build!")
            return False

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed: {e}")
        return False

def create_installer_script():
    """Create an InnoSetup script for professional Windows installer."""

    inno_script = r'''
; ITU Racing - FSAE Signal Analyzer
; InnoSetup Installer Script
;
; To use:
; 1. Download InnoSetup from https://jrsoftware.org/isinfo.php
; 2. Open this .iss file in InnoSetup
; 3. Click Build > Compile

[Setup]
AppName=FSAE Signal Analyzer
AppVersion=2.0
AppPublisher=ITU Racing Electronics
AppPublisherURL=https://github.com/ITU-Racing
DefaultDirName={autopf}\FSAE Signal Analyzer
DefaultGroupName=ITU Racing
OutputDir=installer
OutputBaseFilename=FSAE_Signal_Analyzer_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Uncomment if you have an icon:
; SetupIconFile=assets\icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\FSAE_Signal_Analyzer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\FSAE Signal Analyzer"; Filename: "{app}\FSAE_Signal_Analyzer.exe"
Name: "{group}\{cm:UninstallProgram,FSAE Signal Analyzer}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\FSAE Signal Analyzer"; Filename: "{app}\FSAE_Signal_Analyzer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FSAE_Signal_Analyzer.exe"; Description: "{cm:LaunchProgram,FSAE Signal Analyzer}"; Flags: nowait postinstall skipifsilent
'''

    with open('installer_script.iss', 'w') as f:
        f.write(inno_script)

    print("[*] Created installer_script.iss for InnoSetup")
    print("    Download InnoSetup from: https://jrsoftware.org/isinfo.php")

if __name__ == '__main__':
    print("\nITU Racing - FSAE Signal Analyzer Build System")
    print("-" * 50)
    print("\nOptions:")
    print("  1. Build standalone .exe (PyInstaller)")
    print("  2. Create InnoSetup installer script")
    print("  3. Both")
    print("")

    choice = input("Select option (1/2/3) [default: 1]: ").strip() or "1"

    if choice == "1":
        build_executable()
    elif choice == "2":
        create_installer_script()
    elif choice == "3":
        if build_executable():
            create_installer_script()
    else:
        print("Invalid option. Running default build...")
        build_executable()
