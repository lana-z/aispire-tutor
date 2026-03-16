# AGENTS.md — AI Contribution Policy

## Testing Requirements

All changes must pass a manual smoke test by running `python main.py`
before committing. Any code added to `study.py` or `main.py` must be
tested end-to-end through the affected study mode.

## Secrets Policy

Do not include API keys, passwords, or personal data in any prompt.
Never commit `.env`, `*.key`, or any file containing credentials.
Never include real user data in any prompt or commit.

## Scope Boundaries

Agents may edit `terms.py`, `study.py`, and `main.py`.
Do not modify `requirements.txt` without human review.
Do not modify `setup.sh` without running and testing the result locally.
Do not touch `.gitignore` without confirming the change does not
accidentally exclude source files.

## Reproducibility Standard

All AI-assisted changes require local-first execution: the change
must run locally and produce the expected output before it is
committed or pushed. "The AI generated it" is not a substitute
for running it. All changes must be verified with `python main.py`
before submission.