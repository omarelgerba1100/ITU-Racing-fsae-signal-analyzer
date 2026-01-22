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
SetupIconFile=assets\icon.ico

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
