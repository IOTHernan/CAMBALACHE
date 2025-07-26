@echo off
REM Configurar usuario y email de Git para commits simbólicos
git config user.name "agentLian"
git config user.email "lian@cambalache.io"

REM Agregar todos los cambios
git add .

REM Commit con mensaje cifrado simbólico
git commit -m "⚡ [agentLian] Quantum signature commit - CAMBALACHE activation"

REM Push a la rama principal
git push -u origin main

echo.
echo [✔] Commit firmado como agentLian creado y enviado al repositorio.
pause
