"""Use Claude to extract structured product data from PDF text."""

import json
import os
from anthropic import Anthropic

_client: Anthropic | None = None
_current_key: str | None = None


def set_api_key(api_key: str) -> None:
    """Set (or update) the API key used for extraction."""
    global _client, _current_key
    if api_key != _current_key:
        _client = Anthropic(api_key=api_key)
        _current_key = api_key


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable is not set. "
                "Create a .env file in the backend/ directory or export the variable."
            )
        _client = Anthropic(api_key=api_key)
    return _client


def extract_products(
    pdf_text: str,
    existing_columns: list[str],
    pdf_filename: str = "document.pdf",
    catalog_columns: list[str] | None = None,
    catalog_samples: dict[str, list[str]] | None = None,
) -> list[dict]:
    """Ask Claude to extract product rows from the PDF text.

    When catalog_columns and catalog_samples are provided, Claude will
    intelligently map free-text content (descriptions, features, benefits,
    etc.) into the target catalog columns.

    Returns a list of dicts. Each dict maps column names to values.
    May include keys that are NOT in *existing_columns* — the caller
    is responsible for extending the Excel schema.
    """
    # Build the catalog-aware context block
    if catalog_columns and catalog_samples:
        # Format columns with sample values so Claude understands what goes where
        col_descriptions = []
        for col in catalog_columns:
            samples = catalog_samples.get(col, [])
            if samples:
                examples = ", ".join(f'"{s}"' for s in samples[:3])
                col_descriptions.append(f'  - "{col}" (examples: {examples})')
            else:
                col_descriptions.append(f'  - "{col}"')
        cols_block = "\n".join(col_descriptions)

        columns_hint = (
            "IMPORTANT: The target Excel catalog has these columns:\n"
            f"{cols_block}\n\n"
            "You MUST map extracted data into these exact column names wherever possible.\n"
            "For free-text content in the PDF (descriptions, features, benefits, specs, "
            "marketing copy, bullet points, etc.), intelligently determine which catalog "
            "column each piece of information belongs to based on the column name and the "
            "example values shown above.\n\n"
            "For example:\n"
            '- A "Short Description" in the PDF might map to a catalog column called "Description" or "Short Desc"\n'
            '- "Features and Benefits" text might need to be split across "Features" and "Benefits" columns\n'
            '- Bullet-point specs might map to specific columns like "Weight", "Material", "Dimensions"\n\n'
            "If the PDF contains data that genuinely does not fit ANY existing catalog column, "
            "create a new descriptive column name for it. But prefer mapping to existing columns.\n\n"
        )
    elif existing_columns:
        columns_hint = (
            "The existing Excel catalog has these columns:\n"
            f"{json.dumps(existing_columns)}\n\n"
            "Map extracted data to these columns where applicable. "
            "If the PDF contains attributes that don't fit any existing column, "
            "create NEW descriptive column names for them.\n\n"
        )
    else:
        columns_hint = ""

    prompt = (
        f"You are a product-data extraction assistant.\n\n"
        f"I will give you the raw text extracted from a PDF file named '{pdf_filename}'.\n\n"
        f"{columns_hint}"
        "Extract EVERY product / item you can find and return a JSON array of objects. "
        "Each object represents one product row. Use consistent, descriptive keys.\n\n"
        "Rules:\n"
        "- Return ONLY valid JSON — no markdown fences, no commentary.\n"
        "- If a value is not available, omit the key (don't use null).\n"
        "- For prices, return numbers without currency symbols.\n"
        "- Keep units in a separate key if present (e.g. 'weight_kg').\n"
        "- Be thorough — extract every product you can identify.\n"
        "- For free-text content (descriptions, features, benefits, marketing copy), "
        "parse intelligently: extract individual facts, specs, and attributes into "
        "the most appropriate column rather than dumping everything into one field.\n\n"
        f"--- PDF TEXT START ---\n{pdf_text}\n--- PDF TEXT END ---"
    )

    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # Strip markdown code fences if the model included them anyway
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    products = json.loads(raw)
    if isinstance(products, dict):
        # Model may wrap in {"products": [...]}
        for v in products.values():
            if isinstance(v, list):
                products = v
                break
        else:
            products = [products]

    return products
