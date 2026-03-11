# AIspire Tutor

## Project Overview
AIspire Tutor is a terminal-based study tool designed to help learners review key technical terms through flashcards, quizzes, browsing, and search. It uses a clean command-line interface with Rich formatting to make study sessions more interactive and easier to follow.

## Features
- Flashcard mode for self-review
- Quiz mode with multiple-choice questions
- Browse terms by category
- Search terms by keyword
- Early quit option using `q` in flashcard and quiz sessions
- Session summary showing correct and incorrect answers
- Review table for missed terms

## Files Added and Updated
- `AGENTS.md` — AI contribution policy and repository boundaries
- `CHANGELOG.md` — project change history
- `study.py` — updated to support quitting early with `q`

## Setup Instructions

Clone the repository and move into the project directory:

```bash
git clone https://github.com/osamaharrab/aispire-tutor.git
cd aispire-tutor

python -m venv .venv

# Activate — choose the command for your OS:
# Mac / Linux
source .venv/bin/activate

# Windows Git Bash
source .venv/Scripts/activate

# Windows CMD
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python test_environment.py    # should print "Environment OK"

```
## project Structure

aispire-tutor/
├── AGENTS.md
├── CHANGELOG.md
├── README.md
├── main.py
├── study.py
├── terms.py
├── requirements.txt
└── tests/
```

## Contributing
Work should be done on a feature branch, not on main
Commit messages should be clear and specific
Test changes before opening a pull request

```