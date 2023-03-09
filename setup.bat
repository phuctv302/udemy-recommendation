@echo off
@REM set $script = New-Object Net.WebClient
@REM powershell.exe -Command "& {(New-Object Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')}"
@REM powershell.exe -Command "& iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex"
@REM choco install -y python3
python get-pip.py
echo "Setup successfully! Please run run.bat file to start server"
pause