"""Post-extraction deduplication: merge equivalent columns and duplicate product rows."""

import json
import logging
import re
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

# ── Synonym groups for column name normalization ──────────────────────────
# Each set contains stripped forms (lowercase, no separators) of column names
# that should be treated as the same semantic column.
_SYNONYM_GROUPS: list[set[str]] = [
    {"sku", "productsku", "itemsku"},
    {"productcode", "itemcode", "articlecode", "partcode"},
    {"articlenumber", "partnumber", "itemnumber", "productnumber",
     "partno", "articleno", "itemno"},
    {"productid", "itemid"},
    {"upc", "ean", "barcode", "gtin"},
    {"modelnumber", "modelno"},
    {"brand", "manufacturer", "make"},
]

# Keywords that signal a column is a product identifier
_ID_KEYWORDS = frozenset({
    "sku", "code", "id", "number", "no", "upc", "ean",
    "barcode", "gtin", "part", "article", "item", "model",
    "mpn", "asin", "isbn", "ref", "reference",
})

# Keywords that signal a column is a product name/title
_NAME_KEYWORDS = frozenset({"name", "title", "product", "description"})


# ── Helpers ───────────────────────────────────────────────────────────────

def _strip(col: str) -> str:
    """Lowercase, remove separators, normalise common abbreviations."""
    s = col.lower().strip()
    s = s.replace("#", "number").replace("no.", "number").replace("nr.", "number")
    s = s.replace("_", "").replace("-", "").replace(" ", "").replace(".", "")
    return s


def _is_id_like(col: str) -> bool:
    """True if the column name looks like a product identifier."""
    words = set(col.lower().replace("_", " ").replace("-", " ").split())
    return bool(words & _ID_KEYWORDS)


def _is_name_like(col: str) -> bool:
    """True if the column name looks like a product name/title."""
    words = set(col.lower().replace("_", " ").replace("-", " ").split())
    return bool(words & _NAME_KEYWORDS)


def _synonym_group_for(stripped: str) -> int | None:
    for i, grp in enumerate(_SYNONYM_GROUPS):
        if stripped in grp:
            return i
    return None


def _normalize_id(val) -> str:
    """Normalize an ID value for comparison (lowercase, strip separators)."""
    s = str(val).strip().lower()
    s = s.replace("-", "").replace(" ", "").replace(".", "")
    return s


def _similarity(a: str, b: str) -> float:
    """String similarity ratio 0..1."""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


# Pattern for model-number-like tokens: alphanumeric with optional hyphens,
# containing at least one digit AND one letter (e.g. "WH-1000XM5", "A2882")
_MODEL_RE = re.compile(r"[A-Za-z0-9][\w-]*[A-Za-z0-9]")


def _extract_model_tokens(name: str) -> set[str]:
    """Pull out tokens that look like model numbers / part identifiers."""
    tokens = set()
    for m in _MODEL_RE.finditer(name):
        tok = m.group()
        has_digit = any(c.isdigit() for c in tok)
        has_alpha = any(c.isalpha() for c in tok)
        if has_digit and has_alpha and len(tok) >= 3:
            tokens.add(tok.lower().replace("-", ""))
    return tokens


def _significant_tokens(name: str) -> set[str]:
    """Extract significant word tokens (>=3 chars, lowercased) from a name."""
    words = re.split(r"[\s,;/|·•–—]+", name.lower())
    return {w for w in words if len(w) >= 3}


def _names_match(a: str, b: str) -> bool:
    """Determine if two product names refer to the same product.

    Uses multiple signals:
    1. Substring containment (short name inside long name)
    2. Shared model-number tokens (e.g. "WH-1000XM5" in both)
    3. High token overlap (Jaccard >= 0.5 on significant words)
    4. SequenceMatcher ratio >= 0.75
    """
    a = a.strip()
    b = b.strip()
    if not a or not b:
        return False

    al = a.lower()
    bl = b.lower()

    # 1. Substring containment: shorter name fully inside the longer one
    short, long = (al, bl) if len(al) <= len(bl) else (bl, al)
    if len(short) >= 4 and short in long:
        return True

    # 2. Shared model-number tokens
    models_a = _extract_model_tokens(a)
    models_b = _extract_model_tokens(b)
    if models_a and models_b and (models_a & models_b):
        return True

    # 3. Significant-token Jaccard similarity
    toks_a = _significant_tokens(a)
    toks_b = _significant_tokens(b)
    if toks_a and toks_b:
        jaccard = len(toks_a & toks_b) / len(toks_a | toks_b)
        if jaccard >= 0.5:
            return True

    # 4. SequenceMatcher (handles minor edits / typos)
    if _similarity(a, b) >= 0.75:
        return True

    return False


def _pick_canonical(names: list[str]) -> str:
    """From equivalent column names pick the best canonical one.

    Prefers the shortest name; ties broken alphabetically.
    """
    return min(names, key=lambda n: (len(n), n.lower()))


# ── Column normalisation ─────────────────────────────────────────────────

def _build_column_map(products: list[dict]) -> dict[str, str]:
    """Build {original_col: canonical_col} from synonym groups + value overlap."""
    # Collect all column names (preserving first-seen order)
    all_cols: list[str] = []
    seen: set[str] = set()
    for p in products:
        for c in p:
            if c not in seen:
                all_cols.append(c)
                seen.add(c)

    # ── 1. Group by synonym sets ──
    syn_groups: dict[int, list[str]] = {}
    ungrouped: list[str] = []
    for col in all_cols:
        gid = _synonym_group_for(_strip(col))
        if gid is not None:
            syn_groups.setdefault(gid, []).append(col)
        else:
            ungrouped.append(col)

    # ── 2. Value-based matching for ID-like ungrouped columns ──
    id_cols = [c for c in ungrouped if _is_id_like(c)]

    # Collect normalised value sets per column
    col_values: dict[str, set[str]] = {}
    for col in id_cols:
        vals: set[str] = set()
        for p in products:
            v = p.get(col)
            if v is not None and str(v).strip():
                nv = _normalize_id(v)
                if len(nv) > 1:          # skip trivial single-char values
                    vals.add(nv)
        col_values[col] = vals

    value_groups: list[list[str]] = []
    used: set[str] = set()
    for i, c1 in enumerate(id_cols):
        if c1 in used:
            continue
        group = [c1]
        used.add(c1)
        for c2 in id_cols[i + 1:]:
            if c2 in used:
                continue
            overlap = col_values[c1] & col_values[c2]
            if overlap:
                group.append(c2)
                used.add(c2)
        if len(group) > 1:
            value_groups.append(group)

    # ── 3. Build final mapping ──
    col_map: dict[str, str] = {}

    for _gid, cols in syn_groups.items():
        if len(cols) > 1:
            canonical = _pick_canonical(cols)
            for c in cols:
                col_map[c] = canonical

    for group in value_groups:
        canonical = _pick_canonical(group)
        for c in group:
            col_map[c] = canonical

    return col_map


def _apply_column_map(products: list[dict], col_map: dict[str, str]) -> list[dict]:
    """Rename columns in all products according to the mapping."""
    if not col_map:
        return products

    result = []
    for p in products:
        new_p: dict = {}
        for col, val in p.items():
            canonical = col_map.get(col, col)
            if canonical in new_p:
                # Conflict: keep the longer / more detailed value
                existing = str(new_p[canonical])
                new_val = str(val) if val is not None else ""
                if len(new_val) > len(existing):
                    new_p[canonical] = val
            else:
                new_p[canonical] = val
        result.append(new_p)
    return result


# ── Row deduplication ─────────────────────────────────────────────────────

def _merge_rows(base: dict, other: dict) -> dict:
    """Merge two product dicts for the same product.

    - Missing fields are filled in from the other row.
    - For text fields with both values present, keep the longer one.
    """
    merged = dict(base)
    for col, val in other.items():
        if col not in merged or merged[col] in (None, ""):
            merged[col] = val
        elif val is not None and str(val).strip():
            existing = merged[col]
            if isinstance(val, str) and isinstance(existing, str):
                if len(val) > len(existing):
                    merged[col] = val
    return merged


def _llm_find_duplicate_groups(client, products: list[dict]) -> list[list[int]]:
    """Use Claude to identify duplicate products across languages and naming styles.

    Sends all product data to Haiku in a single call. Returns a list of groups,
    where each group is a list of 0-based product indices that are the same product.
    """
    if len(products) < 2:
        return []

    # Build compact product representations
    lines = []
    for i, p in enumerate(products):
        compact = {k: v for k, v in p.items() if v is not None and str(v).strip()}
        lines.append(f"{i + 1}. {json.dumps(compact, ensure_ascii=False)}")
    product_list = "\n".join(lines)

    prompt = (
        "You are a product deduplication assistant. Below is a numbered list of products "
        "extracted from documents. Some may refer to the same physical product but with "
        "different names, languages, abbreviations, or levels of detail.\n\n"
        "Identify which entries are duplicates (same product, different representation). "
        "Return a JSON array of arrays, where each inner array contains the numbers of "
        "products that are the same. Only include groups of 2 or more. Unique products "
        "should NOT appear.\n\n"
        "Rules:\n"
        "- Same brand + same model/MPN = same product (even with extra description text)\n"
        "- A short product name contained in a longer one = same product\n"
        "- Translations of the same product name across languages = same product\n"
        "- Different products from the same brand are NOT duplicates\n"
        "- Return ONLY valid JSON — no markdown fences, no commentary\n"
        "- If no duplicates exist, return []\n\n"
        f"Products:\n{product_list}"
    )

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if included
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    groups_raw = json.loads(raw)

    # Convert 1-based prompt numbers to 0-based product indices
    result = []
    for group in groups_raw:
        indices = [num - 1 for num in group if 1 <= num <= len(products)]
        if len(indices) >= 2:
            result.append(indices)

    return result


def _ids_conflict(products: list[dict], i: int, j: int, id_cols: list[str]) -> bool:
    """True if products i and j have conflicting (different non-empty) ID values."""
    for col in id_cols:
        vi = str(products[i].get(col, "")).strip().lower()
        vj = str(products[j].get(col, "")).strip().lower()
        if vi and vj and _normalize_id(vi) != _normalize_id(vj):
            return True
    return False


def _merge_duplicate_rows(products: list[dict], client=None) -> list[dict]:
    """Merge rows that represent the same product.

    Uses union-find to cluster products by:
      1. Matching ID values (any ID-like column)
      2. LLM-based matching (if client provided) — handles different languages,
         abbreviations, name variants; falls back to heuristic name similarity
    """
    n = len(products)
    if n <= 1:
        return products

    # Discover column types
    all_cols: set[str] = set()
    for p in products:
        all_cols.update(p.keys())
    id_cols = [c for c in all_cols if _is_id_like(c)]
    name_cols = [c for c in all_cols if _is_name_like(c)]

    # ── Union-Find ──
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    # ── 1. Match by shared ID value ──
    id_index: dict[str, list[int]] = {}     # normalised_value → [indices]
    for i, p in enumerate(products):
        for col in id_cols:
            val = p.get(col)
            if val is not None and str(val).strip():
                nv = _normalize_id(val)
                if len(nv) > 1:
                    id_index.setdefault(nv, []).append(i)

    for _val, indices in id_index.items():
        for k in range(1, len(indices)):
            union(indices[0], indices[k])

    # ── 2. Match by name (LLM-powered, with heuristic fallback) ──
    llm_matched = False
    if client is not None and n >= 2:
        try:
            llm_groups = _llm_find_duplicate_groups(client, products)
            for group in llm_groups:
                for k in range(1, len(group)):
                    i, j = group[0], group[k]
                    if find(i) != find(j) and not _ids_conflict(products, i, j, id_cols):
                        union(i, j)
            llm_matched = True
            logger.info("LLM dedup identified %d duplicate groups", len(llm_groups))
        except Exception as exc:
            logger.warning("LLM dedup failed, falling back to heuristic: %s", exc)

    if not llm_matched and name_cols:
        # Heuristic fallback (no LLM client or LLM call failed)
        for i in range(n):
            for j in range(i + 1, n):
                if find(i) == find(j):
                    continue
                if _ids_conflict(products, i, j, id_cols):
                    continue
                for col in name_cols:
                    ni = str(products[i].get(col, "")).strip()
                    nj = str(products[j].get(col, "")).strip()
                    if ni and nj and _names_match(ni, nj):
                        union(i, j)
                        break

    # ── 3. Collect groups and merge ──
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    result = []
    for indices in groups.values():
        merged = products[indices[0]]
        for idx in indices[1:]:
            merged = _merge_rows(merged, products[idx])
        result.append(merged)

    return result


# ── Public API ────────────────────────────────────────────────────────────

def deduplicate_products(products: list[dict], client=None) -> tuple[list[dict], int]:
    """Normalise columns and merge duplicate product rows.

    Args:
        products: List of product dicts to deduplicate.
        client: Optional Anthropic client for LLM-powered duplicate detection.
                When provided, uses Claude Haiku to identify duplicates across
                languages and naming styles. Falls back to heuristic matching
                if not provided or if the LLM call fails.

    Returns (deduplicated_products, number_of_rows_merged).
    """
    if len(products) <= 1:
        return products, 0

    original_count = len(products)

    # Step 1: Normalise semantically equivalent column names
    col_map = _build_column_map(products)
    products = _apply_column_map(products, col_map)

    # Step 2: Merge duplicate rows (LLM-powered when client available)
    products = _merge_duplicate_rows(products, client=client)

    merged_count = original_count - len(products)
    return products, merged_count
