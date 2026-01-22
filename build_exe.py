#!/usr/bin/env python3
"""
ITU Racing - FSAE Signal Analysis Tool
Build Script for Standalone Executable

This script creates a standalone Windows executable using PyInstaller.
The resulting .exe can be distributed without requiring Python installation.

Usage:
    python build_exe.py           # Interactive mode
    python build_exe.py 1         # Build exe only
    python build_exe.py 2         # Create InnoSetup script only
    python build_exe.py 3         # Build exe + InnoSetup script (CI/CD mode)
    python build_exe.py --ci      # Same as option 3, non-interactive

Requirements:
    pip install pyinstaller

Output:
    dist/FSAE_Signal_Analyzer.exe
"""

import subprocess
import sys
import os
import shutil

# Icon path
ICON_PATH = os.path.join('assets', 'icon.ico')

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

def find_innosetup():
    """Find InnoSetup compiler if installed."""
    # Common InnoSetup installation paths
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Try to find via PATH
    try:
        result = subprocess.run(['where', 'ISCC.exe'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass

    return None

def compile_innosetup(script_path):
    """Compile InnoSetup script if InnoSetup is installed."""
    iscc_path = find_innosetup()

    if not iscc_path:
        print("\n[!] InnoSetup not found. Skipping installer compilation.")
        print("    To create installer, install InnoSetup from: https://jrsoftware.org/isinfo.php")
        print("    Then open installer_script.iss and click Build > Compile")
        return False

    print(f"\n[*] InnoSetup found: {iscc_path}")
    print("[*] Compiling installer...")

    # Create installer output directory
    os.makedirs('installer', exist_ok=True)

    try:
        subprocess.check_call([iscc_path, script_path])

        installer_path = os.path.join('installer', 'FSAE_Signal_Analyzer_Setup.exe')
        if os.path.exists(installer_path):
            size_mb = os.path.getsize(installer_path) / (1024 * 1024)
            print(f"\n[OK] Installer created: {os.path.abspath(installer_path)}")
            print(f"     Size: {size_mb:.1f} MB")
            return True
        else:
            print("[!] Installer compilation completed but output not found")
            return False

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] InnoSetup compilation failed: {e}")
        return False

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
    ]

    # Add icon if it exists
    if os.path.exists(ICON_PATH):
        cmd.append(f'--icon={ICON_PATH}')
        print(f"[OK] Using icon: {ICON_PATH}")
    else:
        print(f"[!] Icon not found at {ICON_PATH}")
        print("    Run 'python create_icon.py' to generate the icon")

    # Hidden imports for customtkinter and other packages
    hidden_imports = [
        'customtkinter',
        'CTkMessagebox',
        'plotly',
        'plotly.express',
        'plotly.graph_objects',
        'pandas',
        'numpy',
        'scipy',
        'scipy.signal',
        'scipy.fft',
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.figure',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'openpyxl',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
    ]

    for imp in hidden_imports:
        cmd.append(f'--hidden-import={imp}')

    # Collect all data for customtkinter (themes, etc.)
    cmd.extend([
        '--collect-all=customtkinter',
        '--collect-all=CTkMessagebox',
    ])

    # Entry point
    cmd.append('run_analyzer.py')

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

    # Check if icon exists for the installer script
    icon_line = ""
    if os.path.exists(ICON_PATH):
        icon_line = f"SetupIconFile={ICON_PATH}"

    inno_script = f'''; ITU Racing - FSAE Signal Analyzer
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
DefaultDirName={{autopf}}\\FSAE Signal Analyzer
DefaultGroupName=ITU Racing
OutputDir=installer
OutputBaseFilename=FSAE_Signal_Analyzer_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
{icon_line}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "dist\\FSAE_Signal_Analyzer.exe"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\FSAE Signal Analyzer"; Filename: "{{app}}\\FSAE_Signal_Analyzer.exe"
Name: "{{group}}\\{{cm:UninstallProgram,FSAE Signal Analyzer}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\FSAE Signal Analyzer"; Filename: "{{app}}\\FSAE_Signal_Analyzer.exe"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\FSAE_Signal_Analyzer.exe"; Description: "{{cm:LaunchProgram,FSAE Signal Analyzer}}"; Flags: nowait postinstall skipifsilent
'''

    script_path = 'installer_script.iss'
    with open(script_path, 'w') as f:
        f.write(inno_script)

    print(f"[OK] Created {script_path} for InnoSetup")

    return script_path

def main():
    """Main entry point with command-line argument support."""

    # Parse command-line arguments for non-interactive mode
    choice = None

    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg in ['1', '2', '3']:
            choice = arg
        elif arg in ['--ci', '-ci', '--auto', '--non-interactive']:
            choice = '3'  # CI/CD mode defaults to building everything
        elif arg in ['--help', '-h']:
            print(__doc__)
            sys.exit(0)

    # Interactive mode if no valid argument provided
    if choice is None:
        print("\nITU Racing - FSAE Signal Analyzer Build System")
        print("-" * 50)
        print("\nOptions:")
        print("  1. Build standalone .exe (PyInstaller)")
        print("  2. Create InnoSetup installer script")
        print("  3. Both (recommended for distribution)")
        print("")

        choice = input("Select option (1/2/3) [default: 1]: ").strip() or "1"

    # Execute based on choice
    if choice == "1":
        build_executable()
    elif choice == "2":
        script_path = create_installer_script()
        print("\n    Download InnoSetup from: https://jrsoftware.org/isinfo.php")
        # Try to compile if InnoSetup is available
        compile_innosetup(script_path)
    elif choice == "3":
        if build_executable():
            script_path = create_installer_script()
            # Automatically compile InnoSetup if available
            compile_innosetup(script_path)
    else:
        print("Invalid option. Running default build...")
        build_executable()

if __name__ == '__main__':
    main()
