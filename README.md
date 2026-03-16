# AIspire Tutor

A Python command-line vocabulary study tool for Module 1 key terms. It features flashcard mode, quiz mode, browse, and search.

## Setup Instructions (Recommended)

To avoid environment issues, **do not** create or activate the virtual environment manually. Instead, use the provided setup script. It handles everything automatically.

## Run this in your terminal (Git Bash is recommended for Windows):

*In Bash*
chmod +x setup.sh
./setup.sh


## ⚠️ Troubleshooting for Windows Users
If you run ./setup.sh and get this error:
Error: [Errno 13] Permission denied: '...\.venv\Scripts\python.exe'

## Why this happens:
This is very common on Windows. It happens if you manually activated a virtual environment before running the script. Windows "locks" the python.exe file, preventing the script from modifying it.

## How to fix it in 3 steps:

1-Unlock the file by deactivating the current environment. Run:
*In Bash*
deactivate

2-Delete the .venv folder completely to start fresh.
3-Run the setup script again:
*In Bash*

chmod +x setup.sh
./setup.sh