"""Post-extraction deduplication: merge equivalent columns and duplicate product rows."""

from difflib import SequenceMatcher

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


def _merge_duplicate_rows(products: list[dict]) -> list[dict]:
    """Merge rows that represent the same product.

    Uses union-find to cluster products by:
      1. Matching ID values (any ID-like column)
      2. High name/title similarity (>= 0.80) when IDs don't conflict
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

    # ── 2. Match by name similarity (when IDs don't conflict) ──
    if name_cols:
        for i in range(n):
            for j in range(i + 1, n):
                if find(i) == find(j):
                    continue  # already grouped

                # Ensure no conflicting IDs
                has_conflict = False
                for col in id_cols:
                    vi = str(products[i].get(col, "")).strip().lower()
                    vj = str(products[j].get(col, "")).strip().lower()
                    if vi and vj and _normalize_id(vi) != _normalize_id(vj):
                        has_conflict = True
                        break
                if has_conflict:
                    continue

                # Check name similarity across all name-like columns
                for col in name_cols:
                    ni = str(products[i].get(col, "")).strip()
                    nj = str(products[j].get(col, "")).strip()
                    if ni and nj and _similarity(ni, nj) >= 0.80:
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

def deduplicate_products(products: list[dict]) -> tuple[list[dict], int]:
    """Normalise columns and merge duplicate product rows.

    Returns (deduplicated_products, number_of_rows_merged).
    """
    if len(products) <= 1:
        return products, 0

    original_count = len(products)

    # Step 1: Normalise semantically equivalent column names
    col_map = _build_column_map(products)
    products = _apply_column_map(products, col_map)

    # Step 2: Merge duplicate rows
    products = _merge_duplicate_rows(products)

    merged_count = original_count - len(products)
    return products, merged_count
