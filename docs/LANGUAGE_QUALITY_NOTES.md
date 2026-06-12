# Language Output Quality Notes

This document tracks known limitations of AI-generated output in Hindi
(`hi`) and Telugu (`te`) compared to English (`en`), per task T027.

## Methodology

For each of the six analysis sections (Hidden Skills, Likely Interview
Questions, Resume Gap Analysis, Interview Readiness Score, Preparation
Plan, Hiring Manager Simulation), a sample job description and resume
were run through the pipeline once per language, using the same
underlying model for all three runs in a given session (Gemini or
Ollama, whichever was active).

## Summary

- **English (`en`)**: Baseline quality. JSON structure (field names,
  category enum values such as `strong_match`/`weak_match`/`missing`)
  is consistently produced exactly as specified, since the prompt
  templates themselves are written in English.
- **Hindi (`hi`)**: Narrative and label *values* (commentary, requirement
  names, question text, preparation topics) are translated correctly in
  the large majority of runs. JSON structure (field names and enum
  values) remains in English as instructed. Occasionally, technical
  terms (e.g. "Docker", "CI/CD", "API") are left in English/transliterated
  within otherwise-Hindi text — this is treated as acceptable, since
  these terms are commonly used as-is in technical Hindi.
- **Telugu (`te`)**: Similar behavior to Hindi — values are translated,
  JSON structure stays in English, technical terms are frequently kept
  in English/transliterated. Telugu output occasionally mixes script
  (Telugu script with embedded Latin-script technical terms), which is
  expected and readable to bilingual technical audiences.

## Known Limitations

1. **Mixed-script technical terms**: Both Hindi and Telugu outputs may
   contain English technical vocabulary (tool names, acronyms) embedded
   in translated sentences. This is a known and accepted limitation —
   fully localizing tool/technology names would reduce clarity for a
   technical audience, not improve it.
2. **JSON field names remain English**: All `parse_response()` functions
   expect JSON keys (e.g. `explicit_requirement`, `category`,
   `priority_label`) and certain enum values (`strong_match`,
   `weak_match`, `missing`) in English regardless of the selected
   language, by design (see each feature module's `build_prompt()`
   docstring). Only the *values* are translated.
3. **Occasional non-compliance with format instructions**: Smaller or
   local models (e.g. via Ollama) are more likely than Gemini to
   occasionally respond with extra commentary, markdown fences, or
   slightly malformed JSON. Each `parse_response()` function handles
   common cases (code-fence stripping) and falls back to a
   user-readable "could not be generated" message
   (`section_unavailable_fallback`) rather than crashing, per NFR-002.
4. **Free-form sections (Hiring Manager Simulation)**: Since
   `hiring_manager_sim` does not require JSON, it is generally the most
   reliably translated section in both Hindi and Telugu.

## Recommendations for Future Work

- If a specific local model is found to struggle with the
  language-instruction approach for `hi`/`te`, consider adding explicit
  few-shot examples to the relevant `build_prompt()` functions for that
  language.
- Consider adding a lightweight post-processing check that flags
  responses where the detected language of `commentary`/`note` fields
  does not match the requested language, so the UI can surface a more
  specific warning than the generic fallback message.