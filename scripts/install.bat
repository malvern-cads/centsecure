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

echo "Installing chocolatey"
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
choco feature enable -n allowGlobalConfirmation
choco upgrade chocolatey
echo "The rest of the script might fail. If it does, please close and open your terminal, then re-run this script."
pause

echo "Installing dependencies (1/2)..."
choco install python
mkdir C:\centsecure\
powershell Expand-Archive centsecure.zip -DestinationPath C:/centsecure
copy requirements.txt C:\centsecure\

cd C:\centsecure\
echo "Installing dependencies (2/2)..."
python -m pip install -r requirements.txt

echo "CentSecure has been installed. To run, change directory to 'C:\centsecure\' and run the command 'python centsecure.py'. Good luck!"