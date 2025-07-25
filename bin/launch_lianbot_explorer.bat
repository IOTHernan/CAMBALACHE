@echo off
cd /d H:\CAMBALACHE\

echo [CAMBALACHE] Booting LianBot Document Explorer...
echo -------------------------------------------- >> logs\lianbot.log
echo %DATE% %TIME% - Launching LianBot >> logs\lianbot.log

REM Asegura que la carpeta de logs exista
if not exist logs (
    mkdir logs
)

REM Abrir navegador automáticamente
start http://localhost:5000

REM Ejecutar el bot Flask con log de salida
python \CAMBALACHE\lianbot\lian_docs.py >> logs\lianbot.log 2>&1

pause
