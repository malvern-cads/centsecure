@echo off

echo ^> Python and Git for windows installer

NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ^> I am running as admin :^)
) ELSE (
    echo ^> This script must be run as admin!
    pause
    exit /b 1
)

echo ^> Downloading python...
powershell $ProgressPreference = 'SilentlyContinue'; wget https://www.python.org/ftp/python/3.7.5/python-3.7.5.exe -OutFile python_install.exe

echo ^> Installing python...
python_install.exe /passive InstallAllUsers=1 PrependPath=1

echo ^> Installing dependencies...
cd "c:\Program Files (x86)\Python*"
python.exe -m pip install colorama pypiwin32
python.exe Scripts/pywin32_postinstall.py -install

echo ^> Python has been installed.

echo ^> GitBash will now be installed
pause

echo ^> Downloading git for windows...
powershell $ProgressPreference = 'SilentlyContinue'; wget https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe -OutFile git_installer.exe

echo ^> Creating config file...
(
echo [Setup]
echo Lang=default
echo Dir=C:\Program Files\Git
echo Group=Git
echo NoIcons=0
echo SetupType=default
echo Components=ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh
echo Tasks=
echo EditorOption=VIM
echo CustomEditorPath=
echo PathOption=Cmd
echo SSHOption=OpenSSH
echo TortoiseOption=false
echo CURLOption=OpenSSL
echo CRLFOption=LFOnly
echo BashTerminalOption=MinTTY
echo PerformanceTweaksFSCache=Enabled
echo UseCredentialManager=Enabled
echo EnableSymlinks=Disabled
echo EnableBuiltinInteractiveAdd=Disabled
)>"win_git.inf"

echo ^> Installing git for windows
git_installer.exe /SP- /SILENT /ALLUSERS /LOADINF="win_git.inf"

echo ^> All done!
pause
