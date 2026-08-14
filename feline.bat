@echo off
setlocal

rem Set the current directory to the script's directory
set SCRIPT_DIR=%~dp0

rem Activate virtual environment
call "%SCRIPT_DIR%\env\Scripts\activate.bat"

rem Execute application
python "%SCRIPT_DIR%\main.py" %*

rem Deactivate virtual environment
deactivate

endlocal
