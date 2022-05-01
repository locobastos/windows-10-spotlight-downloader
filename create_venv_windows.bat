@echo off

:: Checks if Python is installed
python.exe -V >nul 2>&1 || msg * "Python is not installed, please install Python first." && exit 1

:: Creates the Windows virtual environment if not exists
if not exist venv_windows\ (
    echo Creating the Windows virtual environment...
    python.exe -m venv venv_windows
)

:: Prepares the virtual environment
cmd /k "venv_windows\Scripts\activate & pip install -r requirements.txt & exit"
