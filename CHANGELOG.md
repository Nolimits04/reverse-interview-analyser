# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Features

- Project scaffolding, LLM client abstraction (Gemini/Ollama), provider
  selection (BYOK -> local Ollama -> server fallback).
- Resume PDF parsing and English/Hindi/Telugu i18n support.
- Six analysis feature modules: Hidden Skills, Likely Interview
  Questions, Resume Gap Analysis, Interview Readiness Score, Preparation
  Plan, Hiring Manager Simulation.
- Streamlit UI wiring all six analysis sections.

### Testing

- Unit tests for LLM provider factory, resume parser, and feature
  modules.

### Documentation

- README, USER_MANUAL, and language quality notes.