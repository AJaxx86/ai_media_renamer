#!/usr/bin/env bash
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Starting AI Media Renamer..."
python main.py
