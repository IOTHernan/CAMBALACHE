@echo off
setlocal enabledelayedexpansion

REM Define the queue of tasks as batch files or commands
set tasks[1]=setup_agentLian_commit.bat
set tasks[2]=init_push.bat
set tasks[3]=custom_task_3.bat

REM Number of tasks
set taskCount=3

echo CAMBALACHE Task Queue Manager Initialized.
echo.

:loop
if %taskCount% EQU 0 (
    echo All tasks completed.
    goto end
)

for /L %%i in (1,1,%taskCount%) do (
    set task=!tasks[%%i]!
    if exist "!task!" (
        echo Ready to execute: !task!
        echo Press any key to run this task, or CTRL+C to abort.
        pause >nul
        call "!task!"
        echo Task !task! completed.
        echo.
    ) else (
        echo Task file !task! not found, skipping.
    )
)

:end
echo Queue finished. Exiting.
pause
exit /b
