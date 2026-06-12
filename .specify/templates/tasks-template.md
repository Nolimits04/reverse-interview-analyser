# Tasks: [FEATURE NAME]

**Input**: `./plan.md`, `./spec.md`
**Prerequisites**: plan.md Constitution Check passed

## Phase 1: Setup

- [ ] T001 [Project/dependency setup tasks specific to this feature]
- [ ] T002 [Configuration/environment variable additions to
      `.env.example`]

## Phase 2: Tests First (write before implementation)

- [ ] T003 [P] Write unit test(s) for [behavior] in
      `tests/[test_file].py`
- [ ] T004 [P] Write unit test(s) for [edge case] in
      `tests/[test_file].py`

## Phase 3: Core Implementation

- [ ] T005 Implement [module/function] in `[path]`
- [ ] T006 Implement [module/function] in `[path]`

## Phase 4: Integration

- [ ] T007 Wire [feature] into Streamlit UI in `[path]`
- [ ] T008 Connect [feature] to `LLMClient` via `get_llm_client()`

## Phase 5: Polish

- [ ] T009 [P] Add/verify multilingual strings (English/Hindi/Telugu)
- [ ] T010 [P] Update `README.md` / `USER_MANUAL.md` as needed
- [ ] T011 Run ruff, mypy, pytest --cov and fix any issues

## Notes

- [P] = can be done in parallel with other [P] tasks (different files,
  no dependency between them).
- Each task should be small enough to correspond to a single commit.
