@echo off
setlocal

set "TASK_NAME=SMARTPOULTRY Dev Server"
set "STARTUP_LINK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\SMARTPOULTRY Server.lnk"

schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1

if exist "%STARTUP_LINK%" (
    del "%STARTUP_LINK%"
    echo Removed startup shortcut.
)

echo Autostart cleanup complete.
