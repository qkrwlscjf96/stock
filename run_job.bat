@echo off
chcp 65001 > nul

set PYTHON=C:\Users\wlscj\AppData\Local\Programs\Python\Python311\python.exe
set WORKDIR=C:\Users\wlscj\coding\stock\0.code
set SCRIPT=main.py
set LOGDIR=C:\Users\wlscj\coding\stock\99.logs

if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo === START %DATE% %TIME% === >> "%LOGDIR%\job.log"

cd /d "%WORKDIR%"
"%PYTHON%" "%SCRIPT%" >> "%LOGDIR%\job.log" 2>&1

echo Exit Code: %ERRORLEVEL% >> "%LOGDIR%\job.log"
echo === END === >> "%LOGDIR%\job.log"