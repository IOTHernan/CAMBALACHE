@echo off
echo [LianBot] Initializing backend server...
cd /d %~dp0

REM Activar entorno virtual si existe
if exist venv (
    call venv\Scripts\activate
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install flask
)

cd lianbot
start "" http://localhost:5000
python server.py