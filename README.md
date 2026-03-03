# Product Extractor

A full-stack web application that extracts structured product data from virtually any document format using Claude AI and merges the results into Excel catalogs with intelligent column mapping.

## Supported File Types

| Category | Formats |
|----------|---------|
| Documents | PDF, Word (.docx), PowerPoint (.pptx) |
| Spreadsheets | Excel (.xlsx, .xls), CSV, TSV |
| Images (OCR) | PNG, JPG, JPEG, TIFF, BMP, GIF, WEBP |
| Web / Markup | HTML, XML, JSON |
| Plain Text | TXT, LOG, Markdown (.md), reStructuredText (.rst) |

PDFs with no text layer are automatically processed with OCR. Image files are always OCR'd.

## Features

### Multi-Format Extraction
- Upload one or more files of any supported type via drag-and-drop or file picker
- Text-based extraction for documents and structured formats
- Automatic **OCR fallback** (pytesseract) for scanned PDFs and image files
- Claude AI analyzes the extracted text and returns structured product data as JSON
- Per-file status reporting (success/error) without blocking other files

### Excel Catalog Merging
- Optionally upload an existing Excel catalog to merge extracted products into
- Intelligent **column mapping** UI lets you map extracted fields to catalog columns, create new columns, or skip fields
- **Auto-Match** button uses fuzzy matching to suggest column mappings
- Key-column detection (SKU, Part Number, UPC, etc.) for deduplication during merge
- Download the final styled Excel workbook

### Interactive UI
- Single-page browser interface with no framework dependencies
- Drag-and-drop upload zones with visual feedback
- Real-time progress bar during extraction
- Editable data preview tables (first 20 rows)
- Stat cards showing products extracted, files processed, and merge results
- Responsive layout that works on mobile and desktop

### API Key
- Enter your Anthropic API key directly in the browser UI
- The key is sent per-request via header and never stored on the server

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| AI | Anthropic Claude API (claude-sonnet-4-5-20250929) |
| PDF Parsing | pdfplumber, pytesseract (OCR), pdf2image |
| Word / PPTX | python-docx, python-pptx |
| HTML | BeautifulSoup 4 |
| Excel | openpyxl |
| Frontend | Vanilla JavaScript, HTML5, CSS3 |

## Project Structure

```
.
├── index.html              # Single-page frontend application
├── run.sh                  # One-command local startup script
├── backend/
│   ├── main.py             # FastAPI app and route definitions
│   ├── file_parser.py      # Multi-format text extraction (PDF, DOCX, images, etc.)
│   ├── ai_extractor.py     # Claude AI integration for product extraction
│   ├── excel_handler.py    # Excel read, write, and merge logic
│   └── requirements.txt    # Python dependencies
└── docs/
    └── design/             # Design system documentation
```

## Prerequisites

- **Python 3.10+**
- **Anthropic API key** — obtain one at https://console.anthropic.com/
- **Tesseract OCR** (optional, for scanned PDFs and image files) — install via your package manager:
  ```bash
  # Ubuntu / Debian
  sudo apt install tesseract-ocr

  # macOS
  brew install tesseract
  ```

## Getting Started

### Quick Start (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/JordanClarkkk/Claude-code-playground.git
cd Claude-code-playground

# 2. Run
./run.sh
```

The script creates a virtual environment, installs dependencies, and starts the server. Open **http://localhost:8000** in your browser, then paste your Anthropic API key into the input field.

### Manual Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate   # Linux / macOS
# backend\venv\Scripts\activate    # Windows

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start the server
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open **http://localhost:8000** and enter your Anthropic API key in the UI.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/config` | Returns server config (supported file extensions) |
| `POST` | `/api/extract` | Upload files of any supported type and extract products via Claude AI |
| `POST` | `/api/catalog-columns` | Upload an Excel file and retrieve its columns and sample values |
| `POST` | `/api/merge` | Merge extracted products into an Excel catalog using a column mapping |
| `GET` | `/api/download/{job_id}` | Download a generated Excel file |

## Usage Workflow

1. **Enter API key** — Paste your Anthropic API key into the input field at the top of the page.
2. **Upload files** — Drag-and-drop or browse for one or more files containing product data (PDF, Word, images, CSV, etc.).
3. **Extract** — Click "Extract Products" to send the files to Claude AI for analysis. Review the extracted data in the preview table.
4. **Upload a catalog** (optional) — Drag-and-drop an existing Excel catalog to merge into.
5. **Map columns** — Use the column mapping interface to align extracted fields with your catalog structure. Use Auto-Match for quick mapping.
6. **Merge & download** — Click "Merge & Download" to generate the final Excel file.
