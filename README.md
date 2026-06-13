# InterviewIQ (Reverse Interview Analyser)

InterviewIQ flips the usual interview-prep question. Instead of "tell me
about yourself," it asks: **what is this company actually looking for?**

Given a job description (and optionally company information and a
resume), InterviewIQ acts like a hiring manager and produces:

1. **Hidden Skills Detector** — maps explicit JD requirements to inferred
   "hidden" requirements (soft skills, tooling, collaboration norms).
2. **Likely Interview Questions** — company- and role-specific questions,
   grouped by topic.
3. **Resume Gap Analysis** — categorizes each requirement as Strong
   Match / Weak Match / Missing against your resume.
4. **Interview Readiness Score** — technical, communication, domain, and
   overall match percentages with commentary.
5. **Prioritized Preparation Plan** — actionable prep topics grouped into
   priority tiers.
6. **Hiring Manager Simulation** — a candid narrative of likely concerns
   a hiring manager would have about your candidacy.

## Features

- **Bring Your Own Key (BYOK)**: supply your own Gemini API key, used
  only for your session.
- **Local inference support**: if no key is supplied and a local
  [Ollama](https://ollama.com/) instance is running, InterviewIQ uses it
  automatically — no API costs, fully offline.
- **Server fallback**: if neither of the above is available, a
  server-side Gemini key (configured by the operator) is used as a last
  resort.
- **Multilingual**: English, Hindi (हिन्दी), and Telugu (తెలుగు) UI and
  AI-generated output.

## Provider Selection Order

InterviewIQ picks an LLM provider in this fixed order (see
`app/llm/factory.py`):

1. Your Gemini API key, if entered in the sidebar.
2. A local Ollama instance, if reachable at `OLLAMA_HOST`.
3. The server's fallback Gemini API key (`FALLBACK_GEMINI_API_KEY`), if
   configured.

If none of these are available, the app shows an error explaining that
no provider could be resolved.

## Setup

### Requirements

- Python 3.11+
- (Optional) [Ollama](https://ollama.com/) running locally for offline
  inference
- (Optional) A [Google Gemini API key](https://ai.google.dev/) for
  cloud inference

### Install

```bash
git clone <your-fork-or-repo-url>
cd reverse-interview-analyser
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in any values you need:

```bash
cp .env.example .env
```

| Variable                  | Purpose                                                          | Default                  |
| -------------------------- | ----------------------------------------------------------------- | ------------------------- |
| `FALLBACK_GEMINI_API_KEY`  | Server-side Gemini key used only if no user key and no Ollama.   | _(empty)_                 |
| `OLLAMA_HOST`              | Base URL of a local Ollama instance.                             | `http://localhost:11434`  |
| `OLLAMA_MODEL`             | Model name to use with Ollama.                                   | `llama3`                  |
| `GEMINI_MODEL`             | Gemini model name (used for both BYOK and fallback).             | `gemini-2.5-flash`        |

**Never commit a real `.env` file** — it's listed in `.gitignore`.

### Running with Ollama (local inference)

1. Install Ollama: https://ollama.com/download
2. Pull a model (matching `OLLAMA_MODEL`, default `llama3`):
```bash
   ollama pull llama3
```
3. Ollama runs a local server automatically. As long as it's reachable at
   `OLLAMA_HOST` (default `http://localhost:11434`), InterviewIQ will use
   it automatically when no API key is supplied.

### Running with Gemini (BYOK)

1. Get a free API key from [Google AI Studio](https://ai.google.dev/).
2. Enter it in the app's sidebar field, "Your Gemini API key (optional)".
   It is used only for your session and is never stored.

## Usage

```bash
streamlit run app/main.py
```

1. Choose your language (English / Hindi / Telugu) in the sidebar.
2. (Optional) Enter your Gemini API key in the sidebar.
3. Paste the **job description** (required).
4. (Optional) Paste **company information** (about page, website text).
5. (Optional) Upload your **resume** as a PDF.
6. Click **Analyze**.

The app will show which provider is being used, then render all six
analysis sections. If no resume is uploaded, the Resume Gap Analysis and
Interview Readiness Score sections will explain that they're unavailable
for this run, while the other four sections still run.

See [`USER_MANUAL.md`](USER_MANUAL.md) for a detailed walkthrough.

## Development

### Project Structure