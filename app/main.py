"""InterviewIQ Streamlit entrypoint.

Page layout, input collection, provider resolution (FR-005), and
rendering of all six analysis sections (FR-006-FR-011), including
resume-dependent sections being disabled with an explanation when no
resume is provided (spec edge case) and input validation (NFR-002).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.features import (
    gap_analysis,
    hidden_skills,
    hiring_manager_sim,
    interview_questions,
    prep_plan,
    readiness_score,
)
from app.i18n.strings import t
from app.llm.client import LLMClient
from app.llm.factory import get_llm_client
from app.parsing.resume_parser import ResumeParseError, extract_text

LANGUAGES = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "తెలుగు (Telugu)": "te",
}


def _render_hidden_skills(client: LLMClient, jd: str, company_info: str, language: str) -> None:
    st.subheader(t("section_hidden_skills", language))
    prompt = hidden_skills.build_prompt(jd, company_info, language)
    try:
        raw = client.generate(prompt)
    except RuntimeError as exc:
        st.warning(str(exc))
        return

    result = hidden_skills.parse_response(raw)
    if result.is_fallback:
        st.warning(t("section_unavailable_fallback", language))
        return

    st.table(
        [
            {
                t("col_explicit_requirement", language): row.explicit_requirement,
                t("col_hidden_requirement", language): row.hidden_requirement,
            }
            for row in result.rows
        ]
    )


def _render_interview_questions(
    client: LLMClient, jd: str, company_info: str, language: str
) -> None:
    st.subheader(t("section_interview_questions", language))
    prompt = interview_questions.build_prompt(jd, company_info, language)
    try:
        raw = client.generate(prompt)
    except RuntimeError as exc:
        st.warning(str(exc))
        return

    result = interview_questions.parse_response(raw)
    if result.is_fallback:
        st.warning(t("section_unavailable_fallback", language))
        return

    for group in result.groups:
        st.markdown(f"**{group.topic}**")
        for question in group.questions:
            st.markdown(f"- {question}")


_CATEGORY_LABEL_KEYS = {
    "strong_match": "category_strong_match",
    "weak_match": "category_weak_match",
    "missing": "category_missing",
}


def _render_gap_analysis(
    client: LLMClient,
    jd: str,
    resume_text: str | None,
    language: str,
) -> None:
    st.subheader(t("section_gap_analysis", language))

    if not resume_text:
        st.info(t("no_resume_notice", language))
        return

    prompt = gap_analysis.build_prompt(jd, resume_text, language)
    try:
        raw = client.generate(prompt)
    except RuntimeError as exc:
        st.warning(str(exc))
        return

    result = gap_analysis.parse_response(raw)
    if result.is_fallback:
        st.warning(t("section_unavailable_fallback", language))
        return

    st.table(
        [
            {
                t("col_requirement", language): item.requirement,
                t("col_match", language): t(_CATEGORY_LABEL_KEYS[item.category], language),
                t("col_note", language): item.note,
            }
            for item in result.items
        ]
    )


def _render_readiness_score(
    client: LLMClient,
    jd: str,
    resume_text: str | None,
    language: str,
) -> None:
    st.subheader(t("section_readiness_score", language))

    if not resume_text:
        st.info(t("no_resume_notice", language))
        return

    prompt = readiness_score.build_prompt(jd, resume_text, language)
    try:
        raw = client.generate(prompt)
    except RuntimeError as exc:
        st.warning(str(exc))
        return

    result = readiness_score.parse_response(raw)
    if result.is_fallback or result.score is None:
        st.warning(t("section_unavailable_fallback", language))
        return

    score = result.score
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t("metric_technical_match", language), f"{score.technical_match}%")
    col2.metric(t("metric_communication_match", language), f"{score.communication_match}%")
    col3.metric(t("metric_domain_match", language), f"{score.domain_match}%")
    col4.metric(t("metric_overall_readiness", language), f"{score.overall_readiness}%")

    if score.commentary:
        st.markdown(score.commentary)


def _render_prep_plan(
    client: LLMClient,
    jd: str,
    resume_text: str | None,
    language: str,
) -> None:
    st.subheader(t("section_prep_plan", language))
    prompt = prep_plan.build_prompt(jd, resume_text or "", language)
    try:
        raw = client.generate(prompt)
    except RuntimeError as exc:
        st.warning(str(exc))
        return

    result = prep_plan.parse_response(raw)
    if result.is_fallback:
        st.warning(t("section_unavailable_fallback", language))
        return

    for tier in result.tiers:
        st.markdown(f"**{tier.priority_label}**")
        for topic in tier.topics:
            st.markdown(f"- {topic}")


def _render_hiring_manager_sim(
    client: LLMClient,
    jd: str,
    company_info: str,
    resume_text: str | None,
    language: str,
) -> None:
    st.subheader(t("section_hiring_manager_sim", language))
    prompt = hiring_manager_sim.build_prompt(jd, company_info, resume_text or "", language)
    try:
        raw = client.generate(prompt)
    except RuntimeError as exc:
        st.warning(str(exc))
        return

    result = hiring_manager_sim.parse_response(raw)
    if result.is_fallback:
        st.warning(t("section_unavailable_fallback", language))
        return

    st.markdown(result.narrative)


def main() -> None:
    st.set_page_config(page_title="InterviewIQ", page_icon="🎯", layout="wide")

    with st.sidebar:
        language_label = st.selectbox("Language / भाषा / భాష", list(LANGUAGES.keys()))
        language = LANGUAGES[language_label]

    st.title(t("app_title", language))
    st.caption(t("app_tagline", language))

    with st.sidebar:
        st.header(t("settings_header", language))
        user_api_key = st.text_input(t("api_key_label", language), type="password")
        analyze_clicked = st.button(t("analyze_button", language), type="primary")

    st.subheader(t("jd_header", language))
    job_description = st.text_area(t("jd_placeholder", language), height=200)

    st.subheader(t("company_header", language))
    company_info = st.text_area(t("company_placeholder", language), height=120)

    st.subheader(t("resume_header", language))
    resume_file = st.file_uploader(t("resume_uploader", language), type=["pdf"])

    if not analyze_clicked:
        return

    if not job_description.strip():
        st.error(t("error_empty_jd", language))
        return

    resume_text: str | None = None
    if resume_file is not None:
        try:
            resume_text = extract_text(resume_file)
        except ResumeParseError:
            st.error(t("error_resume_unreadable", language))
            resume_text = None

        if resume_text is not None and not resume_text.strip():
            resume_text = None

    try:
        client = get_llm_client(user_gemini_key=user_api_key or None)
    except RuntimeError as exc:
        st.error(str(exc))
        return

    st.info(f"{t('provider_in_use', language)} {client.provider_name}")

    if resume_file is None or not resume_text:
        st.warning(t("no_resume_notice", language))

    with st.spinner(t("running_analysis", language)):
        _render_hidden_skills(client, job_description, company_info, language)
        _render_interview_questions(client, job_description, company_info, language)
        _render_gap_analysis(client, job_description, resume_text, language)
        _render_readiness_score(client, job_description, resume_text, language)
        _render_prep_plan(client, job_description, resume_text, language)
        _render_hiring_manager_sim(client, job_description, company_info, resume_text, language)


if __name__ == "__main__":
    main()
