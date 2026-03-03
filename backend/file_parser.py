"""Extract text content from a wide range of file types.

Supported formats:
  - PDF (.pdf)           — pdfplumber with OCR fallback
  - Images (.png, .jpg, .jpeg, .tiff, .bmp, .gif, .webp) — OCR via pytesseract
  - Word (.docx)         — python-docx
  - PowerPoint (.pptx)   — python-pptx
  - Excel (.xlsx, .xls)  — openpyxl (as tab-separated text)
  - CSV / TSV            — built-in csv module
  - Plain text (.txt, .log, .md, .rst) — raw read
  - HTML (.html, .htm)   — BeautifulSoup
  - JSON (.json)         — built-in json (pretty-printed)
  - XML (.xml)           — built-in ElementTree (text extraction)
"""

import csv
import io
import json
import xml.etree.ElementTree as ET
from pathlib import PurePosixPath

import pdfplumber

try:
    from pdf2image import convert_from_bytes
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    import docx as python_docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from pptx import Presentation
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from openpyxl import load_workbook
from PIL import Image


# ── Public helpers ────────────────────────────────────────────────────────────

SUPPORTED_EXTENSIONS: set[str] = {
    # Documents
    ".pdf", ".docx", ".pptx",
    # Spreadsheets / tabular
    ".xlsx", ".xls", ".csv", ".tsv",
    # Plain text
    ".txt", ".log", ".md", ".rst",
    # Web / markup
    ".html", ".htm", ".xml", ".json",
    # Images (OCR)
    ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp",
}


def is_supported(filename: str) -> bool:
    """Return True if the filename has a supported extension."""
    ext = PurePosixPath(filename).suffix.lower()
    return ext in SUPPORTED_EXTENSIONS


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from *file_bytes* based on *filename* extension.

    Raises ValueError for unsupported types.
    """
    ext = PurePosixPath(filename).suffix.lower()

    if ext == ".pdf":
        return _extract_pdf(file_bytes)
    if ext in {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp"}:
        return _extract_image(file_bytes)
    if ext == ".docx":
        return _extract_docx(file_bytes)
    if ext == ".pptx":
        return _extract_pptx(file_bytes)
    if ext in {".xlsx", ".xls"}:
        return _extract_excel(file_bytes)
    if ext == ".csv":
        return _extract_csv(file_bytes, delimiter=",")
    if ext == ".tsv":
        return _extract_csv(file_bytes, delimiter="\t")
    if ext in {".txt", ".log", ".md", ".rst"}:
        return _extract_plain_text(file_bytes)
    if ext in {".html", ".htm"}:
        return _extract_html(file_bytes)
    if ext == ".json":
        return _extract_json(file_bytes)
    if ext == ".xml":
        return _extract_xml(file_bytes)

    raise ValueError(f"Unsupported file type: {ext}")


# ── Private extractors ────────────────────────────────────────────────────────

def _extract_pdf(pdf_bytes: bytes) -> str:
    text_parts: list[str] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned = [str(cell).strip() if cell else "" for cell in row]
                    page_text += "\n" + "\t".join(cleaned)
            text_parts.append(page_text.strip())

    combined = "\n\n".join(text_parts).strip()

    if len(combined) < 50 and OCR_AVAILABLE:
        combined = _ocr_pdf(pdf_bytes)

    return combined


def _ocr_pdf(pdf_bytes: bytes) -> str:
    images = convert_from_bytes(pdf_bytes, dpi=300)
    ocr_parts: list[str] = []
    for img in images:
        ocr_parts.append(pytesseract.image_to_string(img))
    return "\n\n".join(ocr_parts).strip()


def _extract_image(image_bytes: bytes) -> str:
    if not OCR_AVAILABLE:
        raise RuntimeError(
            "OCR is not available. Install pytesseract and pdf2image to process images."
        )
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img).strip()


def _extract_docx(docx_bytes: bytes) -> str:
    if not DOCX_AVAILABLE:
        raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
    doc = python_docx.Document(io.BytesIO(docx_bytes))

    parts: list[str] = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            parts.append(text)

    # Also extract text from tables
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            parts.append("\t".join(cells))

    return "\n".join(parts).strip()


def _extract_pptx(pptx_bytes: bytes) -> str:
    if not PPTX_AVAILABLE:
        raise RuntimeError("python-pptx is not installed. Run: pip install python-pptx")
    prs = Presentation(io.BytesIO(pptx_bytes))

    parts: list[str] = []
    for slide_num, slide in enumerate(prs.slides, 1):
        slide_texts: list[str] = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if text:
                        slide_texts.append(text)
            if shape.has_table:
                for row in shape.table.rows:
                    cells = [cell.text.strip() for cell in row.cells]
                    slide_texts.append("\t".join(cells))
        if slide_texts:
            parts.append(f"--- Slide {slide_num} ---\n" + "\n".join(slide_texts))

    return "\n\n".join(parts).strip()


def _extract_excel(excel_bytes: bytes) -> str:
    wb = load_workbook(io.BytesIO(excel_bytes), data_only=True)

    parts: list[str] = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        sheet_lines: list[str] = [f"--- Sheet: {ws.title} ---"]
        for row in rows:
            cells = [str(cell).strip() if cell is not None else "" for cell in row]
            sheet_lines.append("\t".join(cells))
        parts.append("\n".join(sheet_lines))

    return "\n\n".join(parts).strip()


def _extract_csv(file_bytes: bytes, delimiter: str = ",") -> str:
    text = file_bytes.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    lines: list[str] = []
    for row in reader:
        lines.append("\t".join(cell.strip() for cell in row))
    return "\n".join(lines).strip()


def _extract_plain_text(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="replace").strip()


def _extract_html(html_bytes: bytes) -> str:
    if not BS4_AVAILABLE:
        raise RuntimeError("beautifulsoup4 is not installed. Run: pip install beautifulsoup4")
    text = html_bytes.decode("utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def _extract_json(json_bytes: bytes) -> str:
    text = json_bytes.decode("utf-8", errors="replace")
    try:
        data = json.loads(text)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return text.strip()


def _extract_xml(xml_bytes: bytes) -> str:
    text = xml_bytes.decode("utf-8", errors="replace")
    try:
        root = ET.fromstring(text)
        parts: list[str] = []
        for elem in root.iter():
            content = (elem.text or "").strip()
            if content:
                tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                parts.append(f"{tag}: {content}")
        return "\n".join(parts).strip() or text.strip()
    except ET.ParseError:
        return text.strip()
