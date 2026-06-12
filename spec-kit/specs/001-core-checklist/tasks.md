# Tasks: Core Interview Readiness Checklist

**Input**: `./plan.md`, `./spec.md`
**Prerequisites**: plan.md Constitution Check passed

## Phase 1: Setup

- [ ] T001 Create project structure (`app/`, `app/llm/`,
      `app/features/`, `app/parsing/`, `app/i18n/`, `tests/`) per
      plan.md Project Structure.
- [ ] T002 Add dependencies via `uv` (streamlit, google-generativeai,
      requests, pymupdf, pytest, pytest-cov, ruff, mypy).
- [ ] T003 [P] Create `app/config.py` for loading environment variables
      (`FALLBACK_GEMINI_API_KEY`, `OLLAMA_HOST`, `OLLAMA_MODEL`).
- [ ] T004 [P] Create `.env.example` documenting required variables
      with no real values.

## Phase 2: Tests First (write before implementation)

- [ ] T005 [P] Write tests for `ollama_is_running()` (reachable /
      unreachable / timeout) in `tests/test_factory.py`.
- [ ] T006 [P] Write tests for `get_llm_client()` provider selection
      order (BYOK key present; no key + Ollama up; no key + Ollama down)
      in `tests/test_factory.py`.
- [ ] T007 [P] Write tests for `resume_parser.extract_text()` against a
      sample PDF (including a corrupt-file error case) in
      `tests/test_resume_parser.py`.
- [ ] T008 [P] Write tests for `hidden_skills.build_prompt()` and
      `parse_response()` (valid JSON and malformed-JSON fallback) in
      `tests/test_hidden_skills.py`.
- [ ] T009 [P] Write tests for `gap_analysis` "no resume provided"
      sentinel behavior in `tests/test_gap_analysis.py`.
- [ ] T010 [P] Write tests for `readiness_score.parse_response()`
      validating presence of technical/communication/domain/overall
      fields in `tests/test_readiness_score.py`.

## Phase 3: Core Implementation

- [ ] T011 Implement `LLMClient` ABC, `GeminiClient`, `OllamaClient` in
      `app/llm/client.py`.
- [ ] T012 Implement `ollama_is_running()` and `get_llm_client()` in
      `app/llm/factory.py`.
- [ ] T013 Implement `resume_parser.extract_text()` in
      `app/parsing/resume_parser.py` using pymupdf, with error handling
      for unsupported/corrupt files.
- [ ] T014 [P] Implement `app/i18n/prompts.py` (language-instruction
      helper, e.g. `language_instruction("hi") -> str`).
- [ ] T015 [P] Implement `app/i18n/strings.py` (UI label lookup for
      English/Hindi/Telugu).
- [ ] T016 Implement `app/features/hidden_skills.py`
      (`build_prompt`, `parse_response`) per FR-006.
- [ ] T017 Implement `app/features/interview_questions.py` per FR-007.
- [ ] T018 Implement `app/features/gap_analysis.py` per FR-008,
      including the "no resume" sentinel result.
- [ ] T019 Implement `app/features/readiness_score.py` per FR-009.
- [ ] T020 Implement `app/features/prep_plan.py` per FR-010.
- [ ] T021 Implement `app/features/hiring_manager_sim.py` per FR-011.

## Phase 4: Integration

- [ ] T022 Implement `app/main.py` page layout: sidebar (language
      selector, API key input, Analyze button), main inputs (job
      description, company info, resume uploader).
- [ ] T023 Wire provider resolution (`get_llm_client()`) into
      `app/main.py` and display the active provider to the user
      (FR-005).
- [ ] T024 Wire all six feature modules into `app/main.py`, rendering
      each section's output (FR-006–FR-011).
- [ ] T025 Implement disabled/explained state for resume-dependent
      sections when no resume is uploaded (spec edge case).
- [ ] T026 Implement input-validation messages for empty job
      description and unparseable resume (NFR-002).

## Phase 5: Polish

- [ ] T027 [P] Verify English/Hindi/Telugu output for each feature
      section; document any known quality limitations (Phase 0 note).
- [ ] T028 [P] Update `README.md` and `USER_MANUAL.md` with setup
      instructions (API key, Ollama setup) and usage walkthrough.
- [ ] T029 Run `ruff`, `mypy`, and `pytest --cov`; resolve any failures
      and ensure coverage reporting is produced.

## Notes

- [P] = can be done in parallel with other [P] tasks (different files,
  no dependency between them).
- Each task should correspond to a single reviewable commit.
