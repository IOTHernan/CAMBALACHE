@echo off
REM Initialize Git repository in current directory
git init

REM Add all files to staging area
git add .

REM Commit changes with message
git commit -m "Initialize CAMBALACHE repository - base structure"

REM Set main branch
git branch -M main

REM Add remote origin with your GitHub username and repository name
git remote add origin https://github.com/IOTHernan/CAMBALACHE.git

REM Push to remote and set upstream
git push -u origin main

echo.
echo [✔] CAMBALACHE successfully initialized and pushed to GitHub under IOTHernan.
pause
