@echo off
echo [LianBot] Initializing backend server...
rem cd /d %~dp0

REM Activar entorno virtual si existe
rem if exist venv (
    call venv\Scripts\activate
rem ) else (
rem     echo Creating virtual environment...
rem     python -m venv venv
rem     call venv\Scripts\activate
rem     pip install flask
rem )

rem cd lianbot
rem start "" http://localhost:5000
python server.py
pause