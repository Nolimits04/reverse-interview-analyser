# InterviewIQ — User Manual

This manual walks through using InterviewIQ to prepare for a specific
job interview.

## 1. Starting the App

If you're running it yourself:

```bash
streamlit run app/main.py
```

This opens InterviewIQ in your browser, usually at
`http://localhost:8501`.

## 2. Choosing Your Language

In the sidebar, use the **Language / भाषा / భాష** dropdown to choose:

- **English**
- **हिन्दी (Hindi)**
- **తెలుగు (Telugu)**

All page labels and AI-generated analysis will be produced in the
selected language. Note that some technical terms (tool names,
acronyms like "API" or "CI/CD") may appear in English/Latin script even
within Hindi or Telugu output — this is intentional, since these terms
are commonly used as-is by technical audiences. See
[`docs/LANGUAGE_QUALITY_NOTES.md`](docs/LANGUAGE_QUALITY_NOTES.md) for
details.

## 3. (Optional) Providing Your Own API Key

If you have a Gemini API key, enter it in the sidebar field labeled
"Your Gemini API key (optional)". This:

- Is used only for your current session.
- Is never written to disk or shared.
- Takes priority over any local Ollama instance or server fallback.

If you don't have a key, leave this blank — see Section 6 below for
what happens next.

## 4. Filling in the Form

### Job Description (required)

Paste the full job description text. The more detail you provide
(responsibilities, requirements, nice-to-haves), the better the
analysis.

### Company Information (optional)

Paste text from the company's "About" page, website, or any other
description of what the company does. This helps tailor the Likely
Interview Questions and Hiring Manager Simulation sections to the
company's actual focus areas (e.g. cloud infrastructure vs. data
analytics).

### Resume (optional)

Upload your resume as a **PDF file**. This enables two additional
sections:

- Resume Gap Analysis
- Interview Readiness Score

If you don't upload a resume, these two sections will display a message
explaining they're unavailable, but the other four sections will still
run using just the job description (and company info, if provided).

If your PDF can't be read (e.g. it's corrupted, password-protected, or
not actually a PDF), you'll see an error message asking you to
re-upload or continue without a resume.

## 5. Running the Analysis

Click **Analyze** in the sidebar. If the job description field is empty,
you'll see an error and analysis won't run.

Once analysis starts, you'll see:

1. A message showing which AI provider is being used (your key, local
   Ollama, or the server fallback).
2. A spinner while each section is generated.
3. Each of the six sections, rendered in order.

## 6. Understanding the Sections

### Hidden Skills

A table mapping each explicit requirement from the job description to
an inferred "hidden" requirement — for example, "Python" might map to
"Debugging ability", or "Communication" might map to "Stakeholder
management".

### Likely Interview Questions

Questions grouped by topic (e.g. Technical Skills, System Design,
Behavioral), tailored to the specific role and company rather than
generic interview questions.

### Resume Gap Analysis

*(Requires a resume.)* A table showing each significant requirement and
whether your resume shows a **Strong Match**, **Weak Match**, or
**Missing**, with a short note explaining the assessment.

### Interview Readiness Score

*(Requires a resume.)* Four percentage metrics — Technical Match,
Communication Match, Domain Match, and Overall Readiness — plus a short
written summary of the biggest factors driving those scores.

### Preparation Plan

A prioritized list of specific topics to study, grouped into tiers
(Priority 1, Priority 2, ...), with Priority 1 being the most urgent.

### Hiring Manager Simulation

A short narrative written from the perspective of the hiring manager,
describing the concerns or open questions they'd likely have about your
candidacy for this specific role.

## 7. Provider Fallback Behavior

InterviewIQ chooses an AI provider in this order:

1. **Your API key** (if entered).
2. **Local Ollama** (if running and reachable — no key needed).
3. **Server fallback key** (configured by whoever is hosting the app).

If none of these work, you'll see an error message explaining that no
AI provider is available, and analysis won't run. In that case:

- Try entering your own Gemini API key, or
- If running InterviewIQ yourself, start Ollama locally (see
  `README.md` for setup instructions).

## 8. If a Section Shows "Could not be generated"

Occasionally, the AI's response for a section may not be in the expected
format (this is more common with smaller local models). When this
happens, that specific section will show a short message saying it
couldn't be generated for this run, while the other sections continue to
display normally. You can try clicking **Analyze** again — results may
vary between runs.

## 9. Privacy Notes

- Your job description, company info, resume text, and (if provided) API
  key are sent to whichever AI provider is selected, for the purpose of
  generating your analysis.
- If using your own API key, requests go directly to that provider using
  your key.
- If using local Ollama, no data leaves your machine.
- If using the server fallback key, requests go to the configured Gemini
  account managed by the app's operator.