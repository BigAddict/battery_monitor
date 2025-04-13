@echo off
REM Battery Monitor Startup Script
REM This script starts the battery monitor in the background

REM Get the directory of this batch file
SET SCRIPT_DIR=%~dp0

REM Start the monitoring script in the background using pythonw
START /B "" pythonw "%SCRIPT_DIR%battery_monitor.py"

REM Exit without showing a command prompt
EXIT
