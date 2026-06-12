# Contributing to InterviewIQ

Thanks for your interest in contributing! This project follows a
spec-driven development workflow (see `.specify/` and `specs/`).

## Getting Started

1. Fork/clone the repository.
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Install pre-commit hooks:
```bash
   pip install pre-commit --break-system-packages
   pre-commit install
```

## Development Workflow

- Each task in `specs/*/tasks.md` should correspond to a single
  reviewable commit.
- Use [Conventional Commits](https://www.conventionalcommits.org/)
  style commit messages (`feat:`, `fix:`, `docs:`, `test:`, `chore:`,
  `refactor:`, `ci:`), since `git-cliff` generates the changelog from
  these.

## Code Style

- Formatting and linting: [`ruff`](https://docs.astral.sh/ruff/)
```bash
  ruff check .
  ruff format .
```
- Type checking: [`mypy`](https://mypy-lang.org/)
```bash
  mypy app
```
- All new functions should have type hints and docstrings (see existing
  modules in `app/` for the expected style).

## Testing

```bash
pytest --cov=app --cov-report=term-missing
```

- New features should include corresponding tests in `tests/`.
- Tests for `parse_response()` functions should cover both valid input
  and malformed/unexpected-format fallback cases (see
  `app/features/*.py` for the `is_fallback` pattern).

## Architectural Principles

Before making changes to `app/llm/` or adding new AI-calling code,
please read
[`.specify/memory/constitution.md`](.specify/memory/constitution.md).
Key points:

- All AI calls must go through the `LLMClient` interface
  (`app/llm/client.py`) — never call a provider SDK directly from a
  feature module.
- Provider selection order (BYOK -> local Ollama -> server fallback) is
  implemented only in `get_llm_client()`
  (`app/llm/factory.py`).
- All user-facing AI-generated text must respect the user's selected
  language (`app/i18n/prompts.py`, `app/i18n/strings.py`).

## Adding a New Language

1. Add the language code to `SUPPORTED_LANGUAGES` and
   `_LANGUAGE_NAMES` in `app/i18n/prompts.py`.
2. Add translations for every key in `_STRINGS` in
   `app/i18n/strings.py`.
3. Add the language to the `LANGUAGES` dict in `app/main.py`.
4. Run a manual smoke test of all six analysis sections in the new
   language and add notes to `docs/LANGUAGE_QUALITY_NOTES.md`.

## Submitting Changes

1. Create a feature branch.
2. Make your changes with clear, atomic commits.
3. Ensure `ruff check .`, `mypy app`, and
   `pytest --cov=app --cov-report=term-missing` all pass.
4. Open a merge request describing what changed and why.