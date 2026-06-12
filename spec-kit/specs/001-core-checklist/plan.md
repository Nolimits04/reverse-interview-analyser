# Implementation Plan: Core Interview Readiness Checklist

**Spec**: `./spec.md`
**Created**: 2026-06-12
**Status**: Draft

## Technical Context

- **Language/Version**: Python 3.11+, managed with `uv`
- **Primary Dependencies**: Streamlit (UI), `google-generativeai` (Gemini
  client), `requests` (Ollama HTTP API), `pymupdf` (PDF text extraction)
- **LLM Providers Touched**: Gemini (BYOK and fallback), Ollama (local)
- **Storage**: None persisted; all data held in Streamlit session state
  for the duration of the session only
- **Testing**: pytest, pytest-cov
- **Target Platform**: Streamlit app, runnable locally and via Docker

## Constitution Check

- [x] Feature accesses LLMs only through `LLMClient` (Principle I) —
      `GeminiClient` and `OllamaClient` both implement `generate()`;
      feature modules call `get_llm_client().generate(prompt)`.
- [x] Provider selection order (BYOK -> Ollama -> fallback key) is
      implemented once, in `get_llm_client()` (Principle II).
- [x] Multilingual output (English/Hindi/Telugu) is addressed via
      prompt-level instruction: each prompt template is parameterized
      with a target-language instruction appended to the request
      (Principle III). UI strings are handled via a simple string
      lookup table per language.
- [x] No secrets written to disk/logs; user-supplied Gemini key lives
      only in `st.session_state`; fallback key read from environment
      variable `FALLBACK_GEMINI_API_KEY`; `.env.example` documents this
      variable (Principle IV).
- [x] No new services/infrastructure: single Streamlit app, optional
      local Ollama dependency (Principle V).
- [x] Tests planned for: provider selection logic, prompt builders,
      resume PDF parsing, and output-section presence (Principle VI).

## Project Structure

```
app/
  main.py                  # Streamlit entrypoint and page layout
  llm/
    __init__.py
    client.py              # LLMClient ABC, GeminiClient, OllamaClient
    factory.py             # get_llm_client(), ollama_is_running()
  features/
    hidden_skills.py        # FR-006
    interview_questions.py  # FR-007
    gap_analysis.py          # FR-008
    readiness_score.py      # FR-009
    prep_plan.py             # FR-010
    hiring_manager_sim.py    # FR-011
  parsing/
    resume_parser.py        # FR-003: PDF -> text
  i18n/
    strings.py               # UI string lookup: en / hi / te
    prompts.py               # language-instruction helper for prompts
  config.py                  # env var loading (.env)
tests/
  test_factory.py
  test_resume_parser.py
  test_hidden_skills.py
  test_gap_analysis.py
  test_readiness_score.py
.env.example                 # FALLBACK_GEMINI_API_KEY=, OLLAMA_HOST=
```

## Phase 0: Research

- **PDF text extraction**: Use `pymupdf` (`fitz`) for resume text
  extraction; it is lightweight and already familiar from prior PDF
  chatbot work. Decision: confirmed, no further research needed.
- **Ollama reachability check**: `GET http://localhost:11434/api/tags`
  (or configurable `OLLAMA_HOST`) with a short timeout (~1s);
  treat any non-200 response or connection error as "not running".
  Decision: confirmed.
- **Multilingual generation quality for Hindi/Telugu**: Gemini and
  Llama-family models via Ollama both support Hindi/Telugu generation
  with explicit instruction, but quality varies by model. Decision:
  start with prompt-level instruction (e.g. "Respond entirely in
  Telugu.") and validate output quality manually; if quality is poor for
  a given local model, document this as a known limitation rather than
  building a separate translation pipeline in v1.
- **Resume gap analysis without resume**: per spec edge case, if no
  resume is provided, `gap_analysis` and `readiness_score` modules
  return a sentinel "not available" result, which the UI renders as a
  disabled/explained section rather than an error.

## Phase 1: Design

### `LLMClient` interface (`app/llm/client.py`)

```python
class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...

class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"): ...

class OllamaClient(LLMClient):
    def __init__(self, host: str, model: str = "llama3"): ...
```

### Provider factory (`app/llm/factory.py`)

```python
def ollama_is_running(host: str) -> bool: ...

def get_llm_client(
    user_gemini_key: str | None,
    ollama_host: str,
    fallback_gemini_key: str,
) -> LLMClient:
    if user_gemini_key:
        return GeminiClient(user_gemini_key)
    if ollama_is_running(ollama_host):
        return OllamaClient(ollama_host)
    return GeminiClient(fallback_gemini_key)
```

### Prompt design

Each feature module exposes `build_prompt(jd, company_info, resume_text,
language) -> str` and `parse_response(raw: str) -> <structured type>`.
Every prompt ends with an explicit language instruction derived from
`i18n/prompts.py`, e.g. "Respond entirely in {language_name}. Do not
include any text in other languages."

Where structured output is needed (tables, scores), prompts instruct
the model to respond in JSON only; `parse_response` parses and validates
this JSON, with a fallback error path per NFR-002.

### UI flow (`app/main.py`)

1. Sidebar: language selector (English/Hindi/Telugu), optional Gemini
   API key input (masked), "Analyze" button.
2. Main area: job description text area, company info text area, resume
   PDF uploader.
3. On "Analyze": resolve provider via `get_llm_client()`, display which
   provider is active, then run each feature module and render its
   section (hidden skills table, questions list, gap analysis table,
   readiness score, prep plan, hiring manager notes).
4. Sections dependent on the resume are disabled with an explanatory
   message if no resume was uploaded (per spec edge case).

## Phase 2: Task Generation Approach

`tasks.md` follows: (1) setup — project structure, config, `.env.example`;
(2) tests first for `llm/factory.py`, `parsing/resume_parser.py`, and one
feature module's prompt/parse pair; (3) core implementation of
`LLMClient`/factory, resume parser, and each of the six feature modules;
(4) integration — wire everything into `app/main.py`, including
language selection and provider indicator; (5) polish — i18n string
coverage for English/Hindi/Telugu UI labels, docs updates, and a final
lint/type/test pass.
