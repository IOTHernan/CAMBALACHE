@echo off
echo === Fuerza 'main' sobre 'master' remoto ===

REM Asegurate de estar en main
git checkout main

REM Verificá que todo esté limpio
git status

REM Fuerza el push: reemplaza el contenido de master con el de main
git push origin +main:master

echo.
echo === ¡master actualizado exitosamente con main! ===

REM Opcional: cambiar a master localmente
git checkout master
git pull origin master
git branch --set-upstream-to=origin/master

pause
