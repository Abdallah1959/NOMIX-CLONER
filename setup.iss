[Setup]
AppName=NOMIX CLONER
AppVersion=3.0.0
AppPublisher=NOMIX Enterprise
DefaultDirName={autopf}\NOMIX CLONER
DefaultGroupName=NOMIX CLONER
OutputDir=Output
OutputBaseFilename=NOMIX_V3_Installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=assets\NOMIXCLONER.ico
UninstallDisplayIcon={app}\NOMIX_CLONER.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
Source: "build_output\NOMIX_CLONER.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"
Name: "{group}\Uninstall NOMIX CLONER"; Filename: "{uninstallexe}"
Name: "{autodesktop}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NOMIX_CLONER.exe"; Description: "Launch NOMIX CLONER"; Flags: nowait postinstall skipifsilent
