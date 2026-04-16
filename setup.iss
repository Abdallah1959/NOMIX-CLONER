[Setup]
; بيانات البرنامج الأساسية
AppName=NOMIX CLONER
AppVersion=3.0.0
AppPublisher=NOMIX Enterprise
AppCopyright=Copyright (C) 2026 NOMIX
DefaultDirName={autopf}\NOMIX CLONER
DefaultGroupName=NOMIX CLONER
OutputDir=Output
OutputBaseFilename=NOMIX_V3_Installer

; إعدادات الشكل والجماليات (الشياكة)
WizardStyle=modern
SetupIconFile=assets\icon.ico
; الصور الجمالية (اختياري: لو عندك صور بانو للبرنامج)
; WizardImageFile=assets\banner.bmp
; WizardSmallImageFile=assets\logo_small.bmp

; الصفحات الإضافية (الشروط والاتفاقيات)
LicenseFile=assets\license.txt
; صوره تظهر قبل التثبيت فيها تعليمات مثلاً
; InfoBeforeFile=assets\readme.txt

; الضغط والأمان
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

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