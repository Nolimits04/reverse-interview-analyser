"""Resume PDF text extraction (FR-003).

Uses pymupdf (`fitz`) to extract text content from an uploaded resume PDF.
"""

from __future__ import annotations

from typing import BinaryIO


class ResumeParseError(Exception):
    """Raised when a resume PDF cannot be parsed."""


def extract_text(file: BinaryIO | bytes) -> str:
    """Extract text content from a PDF resume.

    Args:
        file: A file-like object (e.g. from `st.file_uploader`) or raw
            bytes containing the PDF content.

    Returns:
        The extracted text, with pages joined by double newlines. May be
        an empty string if the PDF contains no extractable text (e.g. a
        scanned image with no OCR layer).

    Raises:
        ResumeParseError: If the file cannot be opened or read as a PDF
            (corrupt, unsupported, or not a PDF).
    """
    try:
        import fitz  # pymupdf
    except ImportError as exc:  # pragma: no cover - import guard
        raise ResumeParseError("PDF parsing library is not available") from exc

    if hasattr(file, "read"):
        data = file.read()
    else:
        data = file

    if not data:
        raise ResumeParseError("Uploaded resume file is empty.")

    try:
        document = fitz.open(stream=data, filetype="pdf")
    except Exception as exc:
        raise ResumeParseError(
            "Could not read the uploaded file as a PDF. Please upload a "
            "valid, non-corrupted PDF resume."
        ) from exc

    try:
        pages_text = []
        for page in document:
            pages_text.append(page.get_text())
    except Exception as exc:
        raise ResumeParseError(
            "An error occurred while extracting text from the resume PDF."
        ) from exc
    finally:
        document.close()

    return "\n\n".join(pages_text).strip()
