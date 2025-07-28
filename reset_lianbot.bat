@echo off
echo Reiniciando Lianbot...

taskkill /IM python.exe /F

timeout /t 2

start python lianbot.py

echo Lianbot reiniciado.
pause
