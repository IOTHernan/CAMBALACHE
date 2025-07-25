@echo off
echo [CAMBALACHE] Setting up Git global config for agentLian...

git config --global user.name "agentLian"
git config --global user.email "lian@cambalache.io"
git config --global core.autocrlf true
git config --global core.ignorecase true
git config --global push.default simple
git config --global pull.rebase false
git config --global merge.conflictstyle diff3
git config --global credential.helper manager-core

REM Optional: Git aliases
git config --global alias.st "status"
git config --global alias.co "checkout"
git config --global alias.ci "commit"
git config --global alias.br "branch"
git config --global alias.lg "log --graph --oneline --decorate --all"

echo.
echo [✔] Git config updated for agentLian. Ready for silent ops.
pause
