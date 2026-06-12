"""Tests for app.parsing.resume_parser (FR-003)."""

from __future__ import annotations

import io

import pytest

from app.parsing.resume_parser import ResumeParseError, extract_text


def _make_pdf_bytes(text: str = "Hello, resume world!") -> bytes:
    """Build a minimal single-page PDF containing `text` using pymupdf."""
    import fitz  # pymupdf

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    data = document.tobytes()
    document.close()
    return data


def test_extract_text_from_valid_pdf_bytes() -> None:
    pdf_bytes = _make_pdf_bytes("Hello, resume world!")
    result = extract_text(pdf_bytes)
    assert "Hello, resume world!" in result


def test_extract_text_from_file_like_object() -> None:
    pdf_bytes = _make_pdf_bytes("File-like resume content")
    file_obj = io.BytesIO(pdf_bytes)
    result = extract_text(file_obj)
    assert "File-like resume content" in result


def test_extract_text_raises_on_empty_input() -> None:
    with pytest.raises(ResumeParseError):
        extract_text(b"")


def test_extract_text_raises_on_corrupt_pdf() -> None:
    with pytest.raises(ResumeParseError):
        extract_text(b"this is definitely not a pdf file")


def test_extract_text_multi_page_joins_with_double_newline() -> None:
    import fitz

    document = fitz.open()
    page1 = document.new_page()
    page1.insert_text((72, 72), "Page one content")
    page2 = document.new_page()
    page2.insert_text((72, 72), "Page two content")
    data = document.tobytes()
    document.close()

    result = extract_text(data)
    assert "Page one content" in result
    assert "Page two content" in result
    assert "\n\n" in result
