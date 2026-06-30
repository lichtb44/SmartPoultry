@echo off
setlocal

set "TASK_NAME=SMARTPOULTRY Dev Server"
set "STARTER=%~dp0start_smartpoultry_server.cmd"

if not exist "%STARTER%" (
    echo Missing startup script: %STARTER%
    exit /b 1
)

schtasks /Create /TN "%TASK_NAME%" /TR "\"%STARTER%\"" /SC ONLOGON /F
if errorlevel 1 (
    echo Failed to install the startup task.
    exit /b 1
)

echo Installed "%TASK_NAME%".
echo The server will start automatically each time you sign in to Windows.
echo URL: http://127.0.0.1:8000/
