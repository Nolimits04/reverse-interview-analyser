# Security Policy

## Supported Versions

This project is under active development. Security fixes are applied to
the latest version on the default branch.

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a
public issue. Instead, report it privately by emailing the maintainers
or using GitLab's confidential issue feature on this project.

Please include:

- A description of the vulnerability and its potential impact.
- Steps to reproduce, including any proof-of-concept code.
- The affected version/commit.

We will acknowledge your report as soon as possible and work with you to
understand and address the issue. Please allow a reasonable amount of
time for a fix before any public disclosure.

## Scope Notes

- **API keys**: InterviewIQ accepts a user-supplied Gemini API key at
  runtime (BYOK). This key is used only for the current session and is
  never written to disk or logs by the application. If you find a code
  path where this key is persisted, logged, or otherwise leaked, please
  report it as a vulnerability.
- **Local inference (Ollama)**: requests to a local Ollama instance stay
  on the user's machine.
- **Dependencies**: dependency vulnerabilities are tracked via
  `pip-audit` in CI/pre-commit. If you find a vulnerable dependency not
  yet flagged, reports are welcome.