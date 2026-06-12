"""UI label lookup table for English, Hindi, and Telugu (Principle III).

Usage:
    from app.i18n.strings import t
    st.title(t("app_title", language))
"""

from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {
    "app_title": {
        "en": "InterviewIQ",
        "hi": "InterviewIQ",
        "te": "InterviewIQ",
    },
    "app_tagline": {
        "en": "AI-powered interview readiness assistant",
        "hi": "एआई-संचालित इंटरव्यू तैयारी सहायक",
        "te": "AI ఆధారిత ఇంటర్వ్యూ సన్నద్ధత సహాయకుడు",
    },
    "settings_header": {
        "en": "Settings",
        "hi": "सेटिंग्स",
        "te": "సెట్టింగ్‌లు",
    },
    "language_label": {
        "en": "Language",
        "hi": "भाषा",
        "te": "భాష",
    },
    "api_key_label": {
        "en": "Your Gemini API key (optional)",
        "hi": "आपकी Gemini API कुंजी (वैकल्पिक)",
        "te": "మీ Gemini API కీ (ఆప్షనల్)",
    },
    "analyze_button": {
        "en": "Analyze",
        "hi": "विश्लेषण करें",
        "te": "విశ్లేషించు",
    },
    "jd_header": {
        "en": "Job Description",
        "hi": "नौकरी का विवरण",
        "te": "ఉద్యోగ వివరణ",
    },
    "jd_placeholder": {
        "en": "Paste the job description",
        "hi": "नौकरी का विवरण पेस्ट करें",
        "te": "ఉద్యోగ వివరణను అతికించండి",
    },
    "company_header": {
        "en": "Company Information (optional)",
        "hi": "कंपनी की जानकारी (वैकल्पिक)",
        "te": "కంపెనీ సమాచారం (ఆప్షనల్)",
    },
    "company_placeholder": {
        "en": "Paste company about/website text",
        "hi": "कंपनी के बारे में/वेबसाइट का टेक्स्ट पेस्ट करें",
        "te": "కంపెనీ గురించి/వెబ్‌సైట్ టెక్స్ట్‌ను అతికించండి",
    },
    "resume_header": {
        "en": "Resume (optional)",
        "hi": "रिज्यूमे (वैकल्पिक)",
        "te": "రెజ్యూమ్ (ఆప్షనల్)",
    },
    "resume_uploader": {
        "en": "Upload your resume (PDF)",
        "hi": "अपना रिज्यूमे अपलोड करें (PDF)",
        "te": "మీ రెజ్యూమ్‌ను అప్‌లోడ్ చేయండి (PDF)",
    },
    "error_empty_jd": {
        "en": "Please provide a job description before analyzing.",
        "hi": "विश्लेषण से पहले कृपया नौकरी का विवरण दें।",
        "te": "విశ్లేషించే ముందు దయచేసి ఉద్యోగ వివరణను అందించండి.",
    },
    "error_resume_unreadable": {
        "en": (
            "We couldn't read your resume PDF. Please try re-uploading "
            "it, or continue without a resume."
        ),
        "hi": ("हम आपका रिज्यूमे PDF नहीं पढ़ सके। कृपया इसे फिर से अपलोड करें, या रिज्यूमे के बिना जारी रखें।"),
        "te": ("మీ రెజ్యూమ్ PDFను చదవలేకపోయాము. దయచేసి దాన్ని మళ్లీ అప్‌లోడ్ చేయండి లేదా రెజ్యూమ్ లేకుండా కొనసాగండి."),
    },
    "provider_in_use": {
        "en": "Using provider:",
        "hi": "उपयोग किया जा रहा प्रदाता:",
        "te": "ఉపయోగిస్తున్న ప్రొవైడర్:",
    },
    "no_resume_notice": {
        "en": (
            "No resume was uploaded, so the resume gap analysis and "
            "interview readiness score are not available for this run."
        ),
        "hi": (
            "कोई रिज्यूमे अपलोड नहीं किया गया, इसलिए इस रन के लिए रिज्यूमे "
            "गैप विश्लेषण और इंटरव्यू तैयारी स्कोर उपलब्ध नहीं हैं।"
        ),
        "te": (
            "రెజ్యూమ్ అప్‌లోడ్ చేయబడలేదు, కాబట్టి ఈ రన్ కోసం రెజ్యూమ్ "
            "గ్యాప్ విశ్లేషణ మరియు ఇంటర్వ్యూ సన్నద్ధత స్కోర్ అందుబాటులో లేవు."
        ),
    },
    "section_hidden_skills": {
        "en": "Hidden Skills",
        "hi": "छिपे हुए कौशल",
        "te": "దాగి ఉన్న నైపుణ్యాలు",
    },
    "col_explicit_requirement": {
        "en": "Explicit Requirement",
        "hi": "स्पष्ट आवश्यकता",
        "te": "స్పష్టమైన అవసరం",
    },
    "col_hidden_requirement": {
        "en": "Hidden Requirement",
        "hi": "छिपी हुई आवश्यकता",
        "te": "దాగి ఉన్న అవసరం",
    },
    "section_interview_questions": {
        "en": "Likely Interview Questions",
        "hi": "संभावित इंटरव्यू प्रश्न",
        "te": "సంభావ్య ఇంటర్వ్యూ ప్రశ్నలు",
    },
    "section_gap_analysis": {
        "en": "Resume Gap Analysis",
        "hi": "रिज्यूमे गैप विश्लेषण",
        "te": "రెజ్యూమ్ గ్యాప్ విశ్లేషణ",
    },
    "col_requirement": {
        "en": "Requirement",
        "hi": "आवश्यकता",
        "te": "అవసరం",
    },
    "col_match": {
        "en": "Match",
        "hi": "मिलान",
        "te": "మ్యాచ్",
    },
    "col_note": {
        "en": "Note",
        "hi": "टिप्पणी",
        "te": "గమనిక",
    },
    "category_strong_match": {
        "en": "Strong Match",
        "hi": "मजबूत मिलान",
        "te": "బలమైన మ్యాచ్",
    },
    "category_weak_match": {
        "en": "Weak Match",
        "hi": "कमजोर मिलान",
        "te": "బలహీనమైన మ్యాచ్",
    },
    "category_missing": {
        "en": "Missing",
        "hi": "गायब",
        "te": "లేదు",
    },
    "section_readiness_score": {
        "en": "Interview Readiness Score",
        "hi": "इंटरव्यू तैयारी स्कोर",
        "te": "ఇంటర్వ్యూ సన్నద్ధత స్కోర్",
    },
    "metric_technical_match": {
        "en": "Technical Match",
        "hi": "तकनीकी मिलान",
        "te": "టెక్నికల్ మ్యాచ్",
    },
    "metric_communication_match": {
        "en": "Communication Match",
        "hi": "संचार मिलान",
        "te": "కమ్యూనికేషన్ మ్యాచ్",
    },
    "metric_domain_match": {
        "en": "Domain Match",
        "hi": "डोमेन मिलान",
        "te": "డొమైన్ మ్యాచ్",
    },
    "metric_overall_readiness": {
        "en": "Overall Readiness",
        "hi": "समग्र तैयारी",
        "te": "మొత్తం సన్నద్ధత",
    },
    "section_prep_plan": {
        "en": "Preparation Plan",
        "hi": "तैयारी योजना",
        "te": "సన్నద్ధత ప్రణాళిక",
    },
    "section_hiring_manager_sim": {
        "en": "Hiring Manager Simulation",
        "hi": "हायरिंग मैनेजर सिमुलेशन",
        "te": "హైరింగ్ మేనేజర్ సిమ్యులేషన్",
    },
    "running_analysis": {
        "en": "Running analysis...",
        "hi": "विश्लेषण चल रहा है...",
        "te": "విశ్లేషణ జరుగుతోంది...",
    },
    "section_unavailable_fallback": {
        "en": "This section could not be generated for this run.",
        "hi": "इस रन के लिए यह सेक्शन तैयार नहीं किया जा सका।",
        "te": "ఈ రన్ కోసం ఈ విభాగాన్ని రూపొందించలేకపోయాము.",
    },
}

DEFAULT_LANGUAGE = "en"


def t(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Look up a UI string by key for the given language.

    Args:
        key: The string key (see `_STRINGS` for available keys).
        language: A language code: "en", "hi", or "te". Falls back to
            English if the key has no translation for this language.

    Returns:
        The localized string, or the key itself wrapped in brackets if
        the key is unknown (to make missing strings visible during
        development rather than crashing).
    """
    entry = _STRINGS.get(key)
    if entry is None:
        return f"[[{key}]]"
    return entry.get(language) or entry.get(DEFAULT_LANGUAGE, f"[[{key}]]")
