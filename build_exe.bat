@echo off
REM build_exe.bat
REM Builds dist\AutoCodeDocFormatting.exe using the venv already set up for
REM this project. Run this from the project root, after run.bat has worked
REM at least once (i.e. venv\ already exists with requirements.txt installed).

cd /d "%~dp0"

if not exist venv\Scripts\activate (
    echo No venv found. Run: python -m venv venv
    echo Then: venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

call venv\Scripts\activate
pip install pyinstaller
pyinstaller AutoCodeDocFormatting.spec

echo.
echo Build finished. If it succeeded, your exe is at dist\AutoCodeDocFormatting.exe
pause