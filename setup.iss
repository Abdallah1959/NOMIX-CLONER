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

; تحديد ملف الترخيص (سيتم تغييره ديناميكياً حسب اللغة)
LicenseFile={tmp}\license_en.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; Flags: unchecked

[Files]
; ملفات البرنامج
Source: "build_output\main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; ملفات الترخيص - سيتم تضمينها داخل المثبّت
Source: "assets\license_en.txt"; Flags: dontcopy
Source: "assets\license_ar.txt"; Flags: dontcopy

[Icons]
Name: "{group}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"
Name: "{group}\Uninstall NOMIX CLONER"; Filename: "{uninstallexe}"
Name: "{autodesktop}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NOMIX_CLONER.exe"; Description: "{cm:LaunchProgram,NOMIX CLONER}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
var
  LicenseFilePath: string;
begin
  { استخراج ملفات الترخيص من داخل المثبّت }
  ExtractTemporaryFile('license_en.txt');
  ExtractTemporaryFile('license_ar.txt');

  { اختيار ملف الترخيص بناءً على اللغة }
  if ActiveLanguage = 'arabic' then
    LicenseFilePath := ExpandConstant('{tmp}\license_ar.txt')
  else
    LicenseFilePath := ExpandConstant('{tmp}\license_en.txt');

  { تحميل نص الاتفاقية }
  WizardForm.LicenseMemo.Lines.LoadFromFile(LicenseFilePath);
end;
