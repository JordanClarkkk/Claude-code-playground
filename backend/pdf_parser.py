"""PDF text extraction — handles both text-based and scanned (OCR) PDFs."""

import io
import pdfplumber

try:
    from pdf2image import convert_from_bytes
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF. Falls back to OCR if text layer is empty."""
    text_parts: list[str] = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            tables = page.extract_tables()
            # Append table rows as tab-separated lines for structured context
            for table in tables:
                for row in table:
                    cleaned = [str(cell).strip() if cell else "" for cell in row]
                    page_text += "\n" + "\t".join(cleaned)
            text_parts.append(page_text.strip())

    combined = "\n\n".join(text_parts).strip()

    # If we got almost no text, try OCR
    if len(combined) < 50 and OCR_AVAILABLE:
        combined = _ocr_pdf(pdf_bytes)

    return combined


def _ocr_pdf(pdf_bytes: bytes) -> str:
    """Run OCR on every page of a PDF."""
    images = convert_from_bytes(pdf_bytes, dpi=300)
    ocr_parts: list[str] = []
    for img in images:
        ocr_parts.append(pytesseract.image_to_string(img))
    return "\n\n".join(ocr_parts).strip()
