@echo off
cd /d "%~dp0smartpoultry"
"%~dp0venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000 --noreload >> "%~dp0server.cmd.log" 2>&1
