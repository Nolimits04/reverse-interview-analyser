# Feature Specification: Core Interview Readiness Checklist

**Feature Branch**: `001-core-checklist`
**Created**: 2026-06-12
**Status**: Draft
**Input**: A candidate provides a job description, optional company
information, and their resume. The system analyzes these inputs and
produces a structured set of interview-preparation outputs ("the
checklist"): hidden requirements, likely interview questions, a resume
gap analysis, an interview readiness score, a prioritized preparation
plan, and a hiring-manager-style risk assessment.

## User Scenarios & Testing

### Primary User Story

A candidate preparing for an interview pastes or uploads a job
description, optionally adds the company's about/website text, and
uploads their resume (PDF). They select a provider option (their own
Gemini API key, or "use local/automatic") and a display language
(English, Hindi, or Telugu). The system returns a single consolidated
"readiness checklist" covering what the company is really looking for,
how the candidate's resume measures up, what questions they're likely to
be asked, and what to do next, all in the selected language.

### Acceptance Scenarios

1. **Given** a valid job description and resume PDF, **When** the user
   clicks "Analyze", **Then** the system displays: a hidden-skills table
   (explicit vs. hidden requirements), a list of likely interview
   questions grouped by topic, a resume gap analysis (strong match / weak
   match / missing), an interview readiness score (technical,
   communication, domain, overall), and a prioritized preparation plan.

2. **Given** the user has not supplied a Gemini API key and Ollama is
   running locally, **When** they click "Analyze", **Then** the system
   uses the local Ollama model and indicates in the UI which provider
   was used.

3. **Given** the user has not supplied a Gemini API key and Ollama is not
   reachable, **When** they click "Analyze", **Then** the system falls
   back to the server-side Gemini key and indicates in the UI which
   provider was used.

4. **Given** the user selects Hindi or Telugu as the display language,
   **When** results are generated, **Then** all analysis sections
   (headings and AI-generated content) are presented in the selected
   language.

5. **Given** valid inputs, **When** the user requests the "hiring manager
   simulation", **Then** the system returns a short narrative of likely
   concerns a hiring manager would have about this candidate for this
   role.

### Edge Cases

- Job description field is empty -> system MUST prompt the user to
  provide a job description before analysis can run.
- Resume PDF cannot be parsed (corrupt/unsupported) -> system MUST show a
  clear error and allow re-upload, without crashing the session.
- Resume is not provided -> system MUST still produce hidden-skills
  analysis and likely questions, but MUST omit/disable the gap analysis
  and readiness score sections (and state why).
- Company information field is empty -> system MUST proceed using only
  the job description.
- Neither a user API key nor a reachable Ollama instance nor a valid
  fallback key is available -> system MUST show a clear configuration
  error rather than failing silently.
- Selected language's translation/generation fails or is partial ->
  system MUST fall back to English for the affected section and indicate
  this to the user.

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept a job description as pasted text.
- **FR-002**: System MUST accept optional company information as pasted
  text (e.g. copied from a company's About page).
- **FR-003**: System MUST accept a resume as an uploaded PDF and extract
  its text content.
- **FR-004**: System MUST allow the user to optionally provide their own
  Gemini API key for the session.
- **FR-005**: System MUST select the LLM provider per the order defined
  in the project constitution (user key -> local Ollama -> fallback key)
  and MUST surface to the user which provider was used for a given
  analysis run.
- **FR-006**: System MUST produce a "Hidden Skills" output: a table
  mapping explicit requirements from the job description to inferred
  hidden requirements (e.g. soft skills, tooling, collaboration
  expectations).
- **FR-007**: System MUST produce a list of likely interview questions,
  tailored to the specific job description and company information
  (not generic boilerplate), grouped by topic/category.
- **FR-008**: System MUST produce a resume gap analysis comparing the
  resume against the job description, categorizing skills/requirements
  as Strong Match, Weak Match, or Missing.
- **FR-009**: System MUST produce an Interview Readiness Score with at
  least: Technical Match, Communication Match, Domain Match, and an
  Overall Readiness percentage.
- **FR-010**: System MUST produce a prioritized preparation plan, grouping
  recommended preparation topics into priority tiers (e.g. Priority 1,
  Priority 2, Priority 3) rather than a flat list.
- **FR-011**: System MUST produce a "hiring manager simulation": a short
  narrative describing likely concerns a hiring manager would have about
  this candidate for this role.
- **FR-012**: System MUST allow the user to select a display/output
  language from: English, Hindi, Telugu, and MUST render both UI labels
  and AI-generated content in that language.
- **FR-013**: System MUST NOT persist the user's API key, resume content,
  or job description beyond the active session.

### Non-Functional Requirements

- **NFR-001**: Analysis for a typical resume + job description (a few
  thousand words combined) SHOULD complete within a time frame
  reasonable for an interactive Streamlit session (target: under 60
  seconds per full analysis run, provider latency permitting).
- **NFR-002**: All error states (parsing failure, provider unreachable,
  missing input) MUST present a user-readable message; the application
  MUST NOT crash or show raw stack traces to the user.

### Key Entities

- **Job Description**: Free-text input describing the role; source of
  explicit and inferred (hidden) requirements.
- **Company Information**: Optional free-text input providing context
  about the company (used to tailor interview questions and hidden
  skills inference).
- **Resume**: Parsed text content extracted from an uploaded PDF;
  source of the candidate's claimed skills/experience.
- **Analysis Result**: The consolidated output of one analysis run,
  composed of: hidden skills table, interview questions list, gap
  analysis table, readiness score, preparation plan, hiring manager
  notes, and the provider/language used to generate it.
- **Provider Configuration**: The resolved choice of LLM provider
  (BYOK Gemini, local Ollama, or fallback Gemini) for a given session.

## Review & Acceptance Checklist

- [ ] No implementation details (frameworks, libraries, code structure)
      in this document.
- [ ] Requirements are testable and unambiguous.
- [ ] Scope is clearly bounded to the core checklist (does not include
      account/auth systems, persistence/history, or analytics).
- [ ] All `NEEDS CLARIFICATION` markers resolved before planning begins.
- [ ] Aligns with project constitution (`.specify/memory/constitution.md`).
