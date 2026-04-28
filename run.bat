@echo off
cd /d "%~dp0"

if not exist .venv (
    echo Creating virtual environment...
    py -m venv .venv
)

call .venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Starting AI Media Renamer...
python main.py

pause
