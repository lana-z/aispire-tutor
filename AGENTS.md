# AGENTS.md — AI Study Tutor AI Agent Governance

> This file defines the rules, constraints, and boundaries for AI agents (Claude, Copilot, Cursor, etc.)
> working in this repository. Any agent reading this file must follow the rules below before taking action.
>
> Last updated: 2026-03-11

---

## Scope

Agents may read any file in this repository needed to understand the project structure, setup instructions,
and application behavior. Agents may modify source files, tests, documentation, and basic setup files when
those changes are directly related to the assigned task.

Agents may create or update files in the following areas:

- `src/`
- `tests/`
- `docs/`
- `README.md`
- `requirements.txt`
- `setup.sh`
- `.gitignore`

Agents may perform the following tasks autonomously:

- Fix small bugs
- Improve documentation
- Add small, self-contained features
- Add or improve tests
- Improve setup and reproducibility
- Refactor code for clarity without changing intended behavior

Agents may suggest changes to repository governance files, workflows, or grading-related files, but must not
modify them without explicit human instruction.

---

## Constraints

- All code changes must remain compatible with Python 3.11.
- Keep changes small, focused, and directly related to the requested task.
- Do not add new dependencies unless they are necessary and clearly justified.
- If a dependency is added, update `requirements.txt` accordingly.
- Follow the existing project structure and naming patterns.
- Preserve current behavior unless the task explicitly requires changing it.
- Do not remove or rewrite another contributor’s work unnecessarily.
- Never commit secrets, credentials, tokens, or `.env` files.
- Do not commit local environment folders such as `.venv/` or cache files such as `__pycache__/`.
- Use clear branch names such as `feature/short-description`, `fix/short-description`, or `docs/short-description`.
- Write clear commit messages in imperative style, for example: `add setup script smoke test`.

---

## Testing Requirements

Before proposing any change as complete, an agent must:

1. Run `bash setup.sh` if the file exists and confirm it exits successfully.
2. Run `pytest tests/ -v` and confirm all tests pass.
3. If no tests exist for the changed behavior, add a reasonable test or clearly state that no automated test was available.
4. Confirm that no unwanted files are staged, including:
   - `.venv/`
   - `.env`
   - `__pycache__/`
   - OS/editor artifact files
5. Verify that the repository still has a clean, reproducible setup flow.

A task is considered done only when:

- The requested change is implemented
- Relevant tests pass
- Setup still works
- Documentation is updated if user-facing behavior changed

---

## Boundaries

- Never read, write, or modify `.env` files or any file containing credentials or secrets.
- Never push to remote branches, open pull requests, merge branches, or delete branches without explicit human instruction.
- Never modify `.github/` workflows, grading files, or automation rules without explicit approval from a human.
- Never modify `AGENTS.md`, `CHANGELOG.md`, or evaluation/rubric files autonomously.
- Never fabricate test results, command output, or completion status.
- Never make grading, approval, or submission decisions on behalf of a human.
- If a task requires deleting tracked files, changing core project structure, or overwriting major existing work, stop and ask for confirmation.
- If the correct action is unclear, prefer leaving a note for a human rather than making a risky change.
