; ==========================================
; DAVID TV - Professional Installer
; ==========================================

[Setup]
AppId={{D3B3A6D7-9C91-4B89-8C9A-DAVIDTV2025}}
AppName=DAVID TV
AppVersion=1.0
AppPublisher=Nexuzy Tech Pvt Ltd
AppPublisherURL=https://nexuzy.tech
AppSupportURL=https://nexuzy.tech
AppUpdatesURL=https://nexuzy.tech

DefaultDirName={pf}\DAVID TV
DefaultGroupName=DAVID TV
AllowNoIcons=yes

OutputBaseFilename=DAVID_TV_Setup
OutputDir=Output
SetupIconFile=icon.ico

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin
UninstallDisplayIcon={app}\DAVID TV.exe
DisableProgramGroupPage=yes

; ==========================================
; Files to Install
; ==========================================

[Files]
Source: "dist\david_tv.exe"; DestDir: "{app}"; DestName: "DAVID TV.exe"; Flags: ignoreversion
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "splash.png"; DestDir: "{app}"; Flags: ignoreversion

; ==========================================
; Start Menu & Desktop Shortcuts
; ==========================================

[Icons]
Name: "{group}\DAVID TV"; Filename: "{app}\DAVID TV.exe"
Name: "{commondesktop}\DAVID TV"; Filename: "{app}\DAVID TV.exe"

; ==========================================
; Run After Install (Optional)
; ==========================================

[Run]
Filename: "{app}\DAVID TV.exe"; Description: "Launch DAVID TV"; Flags: nowait postinstall skipifsilent

; ==========================================
; Uninstall Cleanup
; ==========================================

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

