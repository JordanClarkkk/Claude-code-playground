# PDF Product Extractor

A full-stack web application that extracts structured product data from PDF documents using Claude AI and merges the results into Excel catalogs with intelligent column mapping.

## Features

### PDF Extraction
- Upload one or more PDF files via drag-and-drop or file picker
- Text-based extraction using **pdfplumber** with automatic **OCR fallback** (pytesseract) for scanned documents
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

### API Key Management
- Server-side key via `.env` (recommended) — never exposed to the frontend
- Browser-provided key as fallback when no server key is configured

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| AI | Anthropic Claude API (claude-sonnet-4-5-20250929) |
| PDF Parsing | pdfplumber, pytesseract (OCR), pdf2image |
| Excel | openpyxl |
| Frontend | Vanilla JavaScript, HTML5, CSS3 |

## Project Structure

```
.
├── index.html              # Single-page frontend application
├── run.sh                  # One-command local startup script
├── .env.example            # Environment variable template
├── backend/
│   ├── main.py             # FastAPI app and route definitions
│   ├── ai_extractor.py     # Claude AI integration for product extraction
│   ├── pdf_parser.py       # PDF text extraction with OCR fallback
│   ├── excel_handler.py    # Excel read, write, and merge logic
│   └── requirements.txt    # Python dependencies
└── docs/
    └── design/             # Design system documentation
```

## Prerequisites

- **Python 3.10+**
- **Anthropic API key** — obtain one at https://console.anthropic.com/
- **Tesseract OCR** (optional, for scanned PDFs) — install via your package manager:
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

# 2. Add your API key
cp .env.example .env
# Edit .env and replace sk-ant-... with your real key

# 3. Run
./run.sh
```

The script creates a virtual environment, installs dependencies, and starts the server. Open **http://localhost:8000** in your browser.

### Manual Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate   # Linux / macOS
# backend\venv\Scripts\activate    # Windows

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Start the server
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open **http://localhost:8000**.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | No* | Your Anthropic API key. When set, users don't need to enter a key in the browser. |

*If not set on the server, users must provide a key through the browser UI on each session.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/config` | Returns whether the server has an API key configured |
| `POST` | `/api/extract` | Upload PDFs (+ optional catalog context) and extract products via Claude AI |
| `POST` | `/api/catalog-columns` | Upload an Excel file and retrieve its columns and sample values |
| `POST` | `/api/merge` | Merge extracted products into an Excel catalog using a column mapping |
| `GET` | `/api/download/{job_id}` | Download a generated Excel file |

## Usage Workflow

1. **Enter API key** — If the server doesn't have one configured, paste your key into the input field.
2. **Upload PDFs** — Drag-and-drop or browse for one or more PDF files containing product data.
3. **Extract** — Click "Extract Products" to send the PDFs to Claude AI for analysis. Review the extracted data in the preview table.
4. **Upload a catalog** (optional) — Drag-and-drop an existing Excel catalog to merge into.
5. **Map columns** — Use the column mapping interface to align extracted fields with your catalog structure. Use Auto-Match for quick mapping.
6. **Merge & download** — Click "Merge & Download" to generate the final Excel file.
