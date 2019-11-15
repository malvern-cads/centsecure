@echo off

echo "CentSecure Installer"

NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo "I am running as admin :)"
) ELSE (
    echo "This script must be run as admin!"
    pause
    exit /b 1
)

echo "Downloading python..."
powershell $ProgressPreference = 'SilentlyContinue'; wget https://www.python.org/ftp/python/3.7.5/python-3.7.5.exe -OutFile python_install.exe

echo "Installing python..."
python_install.exe /passive InstallAllUsers=1 PrependPath=1

echo "Installing dependencies..."
cd "c:\Program Files (x86)\Python*"
python.exe -m pip install colorama pypiwin32
python.exe Scripts/pywin32_postinstall.py -install

echo "Python has been installed."
