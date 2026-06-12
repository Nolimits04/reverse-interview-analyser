# Project Constitution

## Project Name

InterviewIQ — an AI-powered interview readiness assistant that analyzes a
job description, a company's public information, and a candidate's resume
to produce a tailored interview preparation package.

## Core Principles

### I. LLM Provider Abstraction (NON-NEGOTIABLE)

All AI interactions MUST go through a single `LLMClient` interface
(`generate(prompt: str, **kwargs) -> str`). Feature modules (hidden skills
detector, gap analysis, risk scoring, prep plan generator, hiring manager
simulator) MUST NOT call any provider SDK or HTTP API directly. New
providers are added by implementing the `LLMClient` interface, never by
branching inside feature code.

### II. Provider Selection Order

The active LLM client is chosen at runtime in this order:

1. User-supplied Gemini API key (Bring Your Own Key), if provided.
2. A locally running Ollama instance, if reachable.
3. A server-side fallback Gemini API key, read from environment
   configuration and never exposed to the client/browser.

This order MUST be implemented in a single factory function
(`get_llm_client(...)`) and MUST NOT be duplicated elsewhere.

### III. Multilingual Output

The application supports English, Hindi, and Telugu. Language selection
applies to both the UI strings and the AI-generated analysis (hidden
skills, gap analysis, risk score commentary, prep plan, hiring manager
feedback). Generated content MUST be produced in the user's selected
language, either via prompt-level instruction or a translation pass —
this decision is documented per-feature in its plan.md.

### IV. Privacy & Security

User-supplied API keys MUST be held only in-memory for the duration of a
session, never written to disk, never logged, and never committed to the
repository. `.env.example` documents required configuration without real
values. Secret scanning (gitleaks) runs in pre-commit and CI.

### V. Simplicity and Incremental Delivery

The application is built as a Streamlit app first. Features are specified,
planned, and broken into tasks individually under `specs/`. Avoid
introducing additional services, frameworks, or infrastructure unless a
feature's plan explicitly justifies the need.

### VI. Test and Quality Gates

Every feature MUST be accompanied by tests sufficient to keep coverage
reporting meaningful. Code MUST pass ruff (lint), mypy (type checking),
and pre-commit hooks before merging.

## Additional Constraints

- Language/runtime: Python 3.11+, dependency management via `uv`.
- Linting: `ruff`. Type checking: `mypy`.
- Secret scanning: `gitleaks` (pre-commit and CI).
- Dependency audit: `uv audit` / `pip-audit` (CI).
- Test framework: `pytest` with `pytest-cov` for coverage.
- Changelog: `git-cliff` (`cliff.toml`), driven by Conventional Commits.
- License: AGPLv3.
- CI: GitLab CI (`.gitlab-ci.yml`) with lint, type_check, test, coverage,
  and format jobs.

## Development Workflow

1. A feature begins as `specs/NNN-feature-name/spec.md` (what and why).
2. Followed by `plan.md` (how, technical context, constitution check).
3. Followed by `tasks.md` (ordered, actionable implementation tasks).
4. Implementation proceeds task-by-task; each task should correspond to a
   reviewable commit.

## Governance

This constitution supersedes ad-hoc practices. Amendments require an
update to this file with a version bump and a note in `CHANGELOG.md`.
All plans and tasks MUST include a "Constitution Check" confirming
compliance with Principles I–VI.

**Version**: 1.0.0 | **Ratified**: 2026-06-12 | **Last Amended**: 2026-06-12
