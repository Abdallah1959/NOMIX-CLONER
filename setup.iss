[Setup]
AppName=NOMIX CLONER
AppVersion=1.0.0
AppPublisher=NOMIX Enterprise
AppCopyright=Copyright (C) 2026 NOMIX Enterprise
DefaultDirName={autopf}\NOMIX CLONER
DefaultGroupName=NOMIX CLONER
OutputDir=Output
OutputBaseFilename=NOMIX_CLONER_V1_Installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=assets\NOMIXCLONER.ico
UninstallDisplayIcon={app}\NOMIX_CLONER.exe
ShowLanguageDialog=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile: "assets\license_en.txt"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"; LicenseFile: "assets\license_ar.txt"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; Flags: unchecked

[Files]
Source: "build_output\main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"
Name: "{group}\Uninstall NOMIX CLONER"; Filename: "{uninstallexe}"
Name: "{autodesktop}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NOMIX_CLONER.exe"; Description: "{cm:LaunchProgram,NOMIX CLONER}"; Flags: nowait postinstall skipifsilent
