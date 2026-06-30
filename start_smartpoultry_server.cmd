@echo off
setlocal

set "ROOT=%~dp0"
set "PROJECT=%ROOT%smartpoultry"
set "PYTHON=%ROOT%venv\Scripts\python.exe"
set "LOG=%ROOT%server.cmd.log"

if not exist "%PYTHON%" (
    echo Python virtual environment was not found: %PYTHON%
    echo Recreate the virtual environment or reinstall dependencies.
    exit /b 1
)

if not exist "%PROJECT%\manage.py" (
    echo Django manage.py was not found: %PROJECT%\manage.py
    exit /b 1
)

cd /d "%PROJECT%" || exit /b 1

echo [%date% %time%] Starting SMARTPOULTRY at http://127.0.0.1:8000/ >> "%LOG%"
"%PYTHON%" manage.py runserver 127.0.0.1:8000 --noreload >> "%LOG%" 2>&1
