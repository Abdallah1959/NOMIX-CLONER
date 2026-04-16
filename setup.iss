[Setup]
; بيانات البرنامج الأساسية
AppName=NOMIX CLONER
AppVersion=3.0.0
AppPublisher=NOMIX Enterprise
DefaultDirName={autopf}\NOMIX CLONER
DefaultGroupName=NOMIX CLONER
OutputDir=Output
OutputBaseFilename=NOMIX_V3_Installer

; إعدادات الشكل والأمان
WizardStyle=modern
SetupIconFile=assets\icon.ico
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
; تفعيل نافذة اختيار اللغة إجبارياً في بداية التسطيب
ShowLanguageDialog=yes

[Languages]
; تعريف اللغات وربط كل لغة بملف الاتفاقية الخاص بها
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile: "assets\license_en.txt"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"; LicenseFile: "assets\license_ar.txt"

[Files]
; الملفات الناتجة من Nuitka
Source: "build_output\main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; أيقونة الديسكتوب وقائمة ابدأ
Name: "{autodesktop}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"; IconFilename: "{app}\NOMIX_CLONER.exe"
Name: "{group}\NOMIX CLONER"; Filename: "{app}\NOMIX_CLONER.exe"
Name: "{group}\{cm:UninstallProgram,NOMIX CLONER}"; Filename: "{uninstaller}"

[Run]
; خيار لفتح البرنامج فور انتهاء التثبيت
Filename: "{app}\NOMIX_CLONER.exe"; Description: "{cm:LaunchProgram,NOMIX CLONER}"; Flags: nowait postinstall skipfs
