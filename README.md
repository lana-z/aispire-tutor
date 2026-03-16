# aispire Vocab Tutor

A command-line vocabulary study tool covering 41 key terms from the aispire Module 1 reading.

## Team Members

- Lana Z (Creator)
- Ameer (Contributor)

## Project Overview

This tool helps learners study and retain Module 1 vocabulary through four interactive modes: flashcards, quiz, browse, and search. It covers 41 terms across 4 categories: Git, Python Env, AI Agents, and Workflow.

## Setup Instructions

Clone the repository and set up the environment:
```bash
git clone <repo-url>
cd aispire-tutor
```

Create and activate a virtual environment:
```bash
python -m venv .venv

# Mac / Linux
source .venv/bin/activate

# Windows Git Bash
source .venv/Scripts/activate

# Windows CMD
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and run:
```bash
pip install -r requirements.txt
python main.py
```

Or use the automated setup script (Git Bash only):
```bash
./setup.sh
```

## Project Structure

aispire-tutor/
├── main.py           — Entry point and menu
├── study.py          — Flashcard and quiz logic
├── terms.py          — All 41 vocabulary terms
├── requirements.txt  — Python dependencies
├── setup.sh          — Automated environment setup
├── AGENTS.md         — AI contribution policy
├── CHANGELOG.md      — Record of notable changes
└── .gitignore        — Files excluded from version control

## Contributing

- Branch naming: `feature/`, `fix/`
- Open a PR to `main` for all changes
- Commit messages: imperative mood, ≤ 50 characters
- Run `python main.py` locally before submitting a PR