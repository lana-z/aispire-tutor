#!/usr/bin/env bash
set -euo pipefail

# Initialize virtual environment
python -m venv .venv

# Activate and install dependencies
# Works for Git Bash on Windows
source .venv/Scripts/activate
pip install -r requirements.txt

# Smoke test
python main.py --help

echo "--------------------------------"
echo "Setup complete! Run 'python main.py' to start."