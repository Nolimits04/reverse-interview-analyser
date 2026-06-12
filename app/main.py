"""InterviewIQ Streamlit entrypoint.

This is an initial skeleton (T022 placeholder): page config, sidebar
inputs, and provider resolution. Feature module wiring (FR-006-FR-011)
and full UI layout will be added in later tasks (T023-T026).
"""

from __future__ import annotations

import streamlit as st

from app.llm.factory import get_llm_client

LANGUAGES = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "తెలుగు (Telugu)": "te",
}


def main() -> None:
    st.set_page_config(page_title="InterviewIQ", page_icon="🎯", layout="wide")

    st.title("InterviewIQ")
    st.caption("AI-powered interview readiness assistant")

    with st.sidebar:
        st.header("Settings")
        language_label = st.selectbox("Language / भाषा / భాష", list(LANGUAGES.keys()))
        language = LANGUAGES[language_label]
        user_api_key = st.text_input("Your Gemini API key (optional)", type="password")
        analyze_clicked = st.button("Analyze", type="primary")

    st.subheader("Job Description")
    job_description = st.text_area("Paste the job description", height=200)

    st.subheader("Company Information (optional)")
    company_info = st.text_area("Paste company about/website text", height=120)

    st.subheader("Resume (optional)")
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if analyze_clicked:
        if not job_description.strip():
            st.error("Please provide a job description before analyzing.")
            return

        try:
            client = get_llm_client(user_gemini_key=user_api_key or None)
        except RuntimeError as exc:
            st.error(str(exc))
            return

        st.info(f"Using provider: {client.provider_name}")
        st.info(f"Selected language: {language_label} ({language})")

        # Feature module wiring (hidden skills, interview questions, gap
        # analysis, readiness score, prep plan, hiring manager sim) and
        # resume parsing are added in subsequent tasks.
        st.write(
            "Analysis pipeline not yet wired up — feature modules "
            "(T016-T021) and integration (T022-T026) are coming next."
        )
        _ = (company_info, resume_file)


if __name__ == "__main__":
    main()
