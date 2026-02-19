"""FastAPI backend for PDF → Excel product extraction."""

import os
import uuid
import json
import traceback
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from pdf_parser import extract_text_from_pdf
from ai_extractor import extract_products, set_api_key
from excel_handler import read_catalog, merge_products, write_catalog

app = FastAPI(title="PDF Product Extractor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Serve the frontend from the repo root
FRONTEND_DIR = Path(__file__).resolve().parent.parent


# ── API Routes ────────────────────────────────────────────────────────────────

@app.post("/api/extract")
async def extract_from_pdfs(
    pdfs: list[UploadFile] = File(...),
    x_api_key: str | None = Header(None),
):
    """Extract products from PDFs without merging. Returns raw product data."""
    api_key = x_api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(400, "No API key provided. Pass it via the UI or set ANTHROPIC_API_KEY env var.")
    set_api_key(api_key)

    all_products: list[dict] = []
    pdf_results: list[dict] = []

    for pdf_file in pdfs:
        pdf_bytes = await pdf_file.read()
        filename = pdf_file.filename or "unknown.pdf"

        try:
            text = extract_text_from_pdf(pdf_bytes)
            if not text:
                pdf_results.append({
                    "filename": filename,
                    "status": "error",
                    "message": "Could not extract any text from PDF",
                    "products_found": 0,
                })
                continue

            products = extract_products(text, [], filename)
            all_products.extend(products)
            pdf_results.append({
                "filename": filename,
                "status": "success",
                "products_found": len(products),
            })
        except Exception as e:
            traceback.print_exc()
            pdf_results.append({
                "filename": filename,
                "status": "error",
                "message": str(e),
                "products_found": 0,
            })

    # Discover all columns across products
    columns: list[str] = []
    seen: set[str] = set()
    for p in all_products:
        for k in p.keys():
            if k not in seen:
                columns.append(k)
                seen.add(k)

    return {
        "pdf_results": pdf_results,
        "products": all_products,
        "columns": columns,
        "total_products": len(all_products),
    }


@app.post("/api/catalog-columns")
async def catalog_columns(
    excel: UploadFile = File(...),
):
    """Read an Excel catalog and return its column names with sample values."""
    excel_bytes = await excel.read()
    if not excel_bytes:
        raise HTTPException(400, "Empty Excel file.")

    columns, rows = read_catalog(excel_bytes)

    # Build sample values (up to 3 non-empty values per column)
    samples: dict[str, list[str]] = {}
    for col in columns:
        vals = []
        for row in rows:
            v = row.get(col)
            if v is not None and str(v).strip():
                vals.append(str(v).strip())
                if len(vals) >= 3:
                    break
        samples[col] = vals

    return {
        "columns": columns,
        "samples": samples,
        "total_rows": len(rows),
    }


@app.post("/api/merge")
async def merge_to_catalog(
    request: Request,
    excel: UploadFile | None = File(None),
):
    """Merge extracted products into a catalog with column mapping."""
    form = await request.form()
    payload_raw = form.get("payload")
    if not payload_raw:
        raise HTTPException(400, "Missing 'payload' field with products and column mapping.")

    try:
        payload = json.loads(payload_raw)
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON in 'payload' field.")

    products: list[dict] = payload.get("products", [])
    # column_mapping: {extracted_col: catalog_col | "__new__" | "__skip__"}
    column_mapping: dict[str, str] = payload.get("column_mapping", {})

    if not products:
        raise HTTPException(400, "No products to merge.")

    # Apply column mapping: rename/filter product keys
    mapped_products = []
    for p in products:
        mapped = {}
        for ext_col, val in p.items():
            target = column_mapping.get(ext_col, ext_col)  # default: keep as-is
            if target == "__skip__":
                continue
            if target == "__new__":
                target = ext_col  # keep the original name as a new column
            mapped[target] = val
        mapped_products.append(mapped)
    products = mapped_products

    # Read existing Excel catalog if provided
    excel_file = form.get("excel")
    existing_columns: list[str] = []
    existing_rows: list[dict] = []
    if excel_file and hasattr(excel_file, "read"):
        excel_bytes = await excel_file.read()
        if excel_bytes:
            existing_columns, existing_rows = read_catalog(excel_bytes)

    # Merge
    final_columns, merged_rows, stats = merge_products(
        existing_columns, existing_rows, products,
    )

    # Write output Excel
    job_id = uuid.uuid4().hex[:12]
    output_bytes = write_catalog(final_columns, merged_rows, stats["new_columns"])
    output_path = OUTPUT_DIR / f"catalog_{job_id}.xlsx"
    output_path.write_bytes(output_bytes)

    # Build preview (first 20 rows)
    preview_rows = merged_rows[:20]
    preview = [
        {col: row.get(col, "") for col in final_columns}
        for row in preview_rows
    ]

    return {
        "job_id": job_id,
        "stats": stats,
        "columns": final_columns,
        "preview": preview,
        "total_rows": len(merged_rows),
        "download_url": f"/api/download/{job_id}",
    }


@app.get("/api/download/{job_id}")
async def download(job_id: str):
    """Download the generated Excel file."""
    path = OUTPUT_DIR / f"catalog_{job_id}.xlsx"
    if not path.exists():
        raise HTTPException(404, "File not found — it may have expired.")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"product_catalog_{job_id}.xlsx",
    )


# Serve frontend (index.html) at root
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
