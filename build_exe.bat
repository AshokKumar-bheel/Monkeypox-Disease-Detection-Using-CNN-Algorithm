@echo off
echo Building MonkeyPox Detector EXE...
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

echo Building EXE file...
pyinstaller --noconfirm --onefile --windowed --name "MonkeyPox_Detector" --icon=icon.ico main.py

echo.
echo Build complete!
echo The EXE file is located in the 'dist' folder.
echo.
pause