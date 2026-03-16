#!/usr/Scripts/env bash
set -euo pipefail

# Initialize virtual environment
echo "Creating virtual environment..."

python -m venv .venv

# Activate and install dependencies
# Works for Git Bash on Windows
echo "Activating virtual environment..."

source .venv/Scripts/activate

echo "Installing requirements..."

pip install -r requirements.txt

# Smoke test
python main.py --help

echo "--------------------------------"
echo "Setup complete! Run 'python main.py' to start."