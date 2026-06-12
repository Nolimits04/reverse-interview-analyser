# AGENTS.md

Guidance for AI coding agents (and humans) working on this repository.

## Project Overview

InterviewIQ is a Streamlit app that analyzes a job description (plus
optional company info and resume) and produces interview-prep content
via an LLM. See `README.md` for the feature overview and
`specs/001-core-checklist/spec.md` for the full functional spec.

## Spec-Driven Development

This project uses a spec-kit workflow:

- `.specify/memory/constitution.md` — governing architectural
  principles. **Read this before modifying `app/llm/` or any
  AI-calling code.**
- `specs/001-core-checklist/spec.md` — functional requirements (FR-xxx)
  and non-functional requirements (NFR-xxx).
- `specs/001-core-checklist/plan.md` — technical plan and project
  structure.
- `specs/001-core-checklist/tasks.md` — the task breakdown; each task
  maps to one commit.

When implementing a new feature, check whether it maps to an existing
FR/NFR or task. If not, consider whether a new spec entry should be
added first.

## Non-Negotiable Rules

1. **LLMClient interface only**: Never call `google.generativeai`,
   `requests` to an Ollama endpoint, or any other provider SDK/API
   directly from a feature module (`app/features/*.py`) or
   `app/main.py`. Always go through
   `app.llm.factory.get_llm_client(...).generate(prompt)`.

2. **Provider selection order is fixed**: BYOK Gemini key -> local
   Ollama (if reachable) -> server fallback Gemini key. This logic lives
   only in `app/llm/factory.get_llm_client()`. Do not duplicate or
   reimplement this logic elsewhere.

3. **Language compliance**: Any new AI-generated, user-facing text must
   end its prompt with `app.i18n.prompts.language_instruction(language)`
   (or equivalent), and any new UI strings must be added to
   `app.i18n.strings._STRINGS` for all supported languages (`en`, `hi`,
   `te`).

4. **Graceful fallback on bad LLM output (NFR-002)**: Every
   `parse_response()` function must handle malformed/unexpected LLM
   output by returning a result object with `is_fallback = True` (or
   equivalent), never by raising an unhandled exception. `app/main.py`
   must render `section_unavailable_fallback` (or similar) in that case,
   not crash.

5. **No secrets in code or fixtures**: Never hard-code API keys, even
   for tests. Tests must mock `LLMClient`/`requests` rather than make
   real network calls.

## Code Conventions

- Python 3.11+, full type hints, Google-style docstrings (see any file
  in `app/` for the expected format).
- `ruff` for linting/formatting, `mypy` for type checking — both run in
  CI and pre-commit. Run them locally before committing.
- One task from `tasks.md` = one commit, using Conventional Commits
  prefixes (`feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`,
  `ci:`).

## Testing Expectations

- New `app/features/*.py` modules need a corresponding
  `tests/test_*.py` covering:
  - `build_prompt()` includes expected inputs and the language
    instruction.
  - `parse_response()` handles valid JSON, malformed JSON, and
    edge cases (empty arrays, missing fields, out-of-range values).
- New `app/llm/` changes need tests mocking the underlying
  `requests`/SDK calls — never call real external services in tests.

## Things Agents Should NOT Do

- Do not add new top-level dependencies without updating both
  `requirements.txt` and `pyproject.toml`.
- Do not remove or weaken the provider-selection fallback chain.
- Do not commit `.env`, API keys, or any other secrets.
- Do not bypass `LLMClient` "just for this one case."