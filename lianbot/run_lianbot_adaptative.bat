@echo off
setlocal ENABLEEXTENSIONS

REM Detect OS (Windows or WSL/Linux/macOS)
ver | findstr /i "Windows" >nul
if %ERRORLEVEL%==0 (
    echo [LianBot] Detected: Windows OS
    echo [LianBot] Initializing virtual environment...

    cd /d %~dp0

    REM Crear entorno virtual si no existe
    if not exist venv (
        echo [LianBot] Creating venv...
        python -m venv venv
    )

    call venv\Scripts\activate
    pip install --quiet flask

    cd lianbot
    start "" http://localhost:5000
    python server.py

) else (
    echo [LianBot] Detected: UNIX-like OS
    cd "$(dirname "$0")"

    if [ ! -d "venv" ]; then
        echo "[LianBot] Creating Python virtual environment..."
        python3 -m venv venv
    fi

    source venv/bin/activate
    pip install --quiet flask

    cd lianbot
    xdg-open http://localhost:5000 2>/dev/null || open http://localhost:5000
    python3 server.py
)

endlocal