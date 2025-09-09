import re
from pathlib import Path
import sys

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

from pdfminer.high_level import extract_text

DEFAULT_PDF = Path(r"d:/data/zxflab/zxflab.com/zxflab.com/assets/publications/第一作者/2014 - GBE - Divergent and Conserved Elements Comprise the Chemoreceptive Repertoire of the Nonblood-Feeding Mosquito Toxorhynchites amboinensis.pdf")

needle = "Xiaofan Zhou"

def clean_text(s: str) -> str:
    s = s.replace('\u00ad', '')  # soft hyphen
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def try_pymupdf(path: Path) -> str | None:
    if not fitz:
        return None
    try:
        doc = fitz.open(path)
        text = []
        for page in doc:
            text.append(page.get_text())
        return "\n".join(text)
    except Exception:
        return None


def try_pdfminer(path: Path) -> str | None:
    try:
        return extract_text(str(path))
    except Exception:
        return None


def extract_authors(full_text: str) -> list[str]:
    # Heuristics: authors usually appear near the beginning. Limit to first ~5000 chars for speed
    head_raw = full_text[:5000]
    lines = [l.strip() for l in head_raw.splitlines() if l.strip()]
    candidates: list[str] = []
    for L in lines:
        if 'Zhou' in L and (',' in L or ' and ' in L):
            candidates.append(clean_text(L))
        elif (L.count(',') >= 2 or ' and ' in L or '&' in L) and 10 < len(L) < 800:
            # Potential author line
            candidates.append(clean_text(L))
    # Deduplicate preserving order
    seen = set()
    uniq = []
    for c in candidates:
        if c not in seen:
            uniq.append(c)
            seen.add(c)
    with_needle = [c for c in uniq if needle in c]
    if with_needle:
        return with_needle
    return uniq[:3]


def parse_author_names(lines: list[str]) -> list[str]:
    full = clean_text(" \n ".join(lines))
    # Anchor around the known author token to avoid matching title/species names
    anchor = re.search(r"X\s*iaofan\s+Zhou", full, flags=re.IGNORECASE)
    if not anchor:
        anchor = re.search(r"Zhou\b", full)
    if not anchor:
        text = full
    else:
        start = max(0, anchor.start() - 200)
        text = full[start:]

    # Stop at common markers that indicate the end of author list / start of affiliations or abstract
    stop_markers = [
        "*Corresponding author",
        "Corresponding author",
        "Accepted:",
    "approved ",
    "Edited by",
    "received for review",
        "Abstract",
    "1Department",
    "Department",
    "aDepartment",
        "Vanderbilt University",
        "GBE",
    ]
    stop_idx = len(text)
    for m in stop_markers:
        i = text.find(m)
        if i != -1:
            stop_idx = min(stop_idx, i)
    text = text[:stop_idx]

    # Normalize separators
    text = text.replace(" and ", ", ")
    # Remove footnote markers glued to names (digits, *, y, dagger) after spaces or directly after letters
    text = re.sub(r"([A-Za-z\.])\s*[0-9,*y†‡]+", r"\1", text)
    # Remove trailing single-letter footnote suffixes attached to surnames (e.g., 'Zwiebela' -> 'Zwiebel')
    text = re.sub(r"\b([A-Z][a-z]+(?: [A-Z]\.)?(?: [A-Z][a-z]+)+)[a-z]{1,2}\b", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip(", ")

    # Split by commas then clean tokens
    tokens = [t.strip() for t in text.split(",") if t.strip()]

    def looks_like_name(tok: str) -> bool:
        # At least two words, mostly capitalized initials or names
        words = tok.split()
        if len(words) < 2 or len(words) > 5:
            return False
        # Avoid obvious non-names
        bad = {"Divergent", "Conserved", "Elements", "Chemoreceptive", "Repertoire", "Mosquito", "Toxorhynchites", "amboinensis"}
        if any(w in bad for w in words):
            return False
        name_token = re.compile(r"^(?:[A-Z][a-z]+|[A-Z]\.|[A-Z]{2,}|[A-Z][a-z]+-[A-Z][a-z]+)$")
        cap_ratio = sum(1 for w in words if name_token.match(w)) / len(words)
        if cap_ratio < 0.5:
            return False
        return True

    names = []
    seen = set()
    for tok in tokens:
        # Remove trailing footnote letters/digits like a,b,c,1,2,* after a name
        tok = re.sub(r"([A-Za-z\.])(?:[ ,]*(?:[a-z]|\d|[*†‡y])+)$", r"\1", tok)
        tok = tok.strip()
        # Fix common broken hyphenation cases observed in PDFs
        tok = tok.replace("Malp artida", "Malpartida")
        if looks_like_name(tok) and tok not in seen:
            names.append(tok)
            seen.add(tok)
    return names


def get_authors_from_pdf(path: Path) -> list[str]:
    text = None
    if fitz:
        text = try_pymupdf(path)
    if not text:
        text = try_pdfminer(path)
    if not text:
        return []
    authors_lines = extract_authors(text)
    names = parse_author_names(authors_lines)
    return names


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF
    if not path.exists():
        print("ERROR: File not found: " + str(path), file=sys.stderr)
        sys.exit(2)
    names = get_authors_from_pdf(path)
    if not names:
        print("ERROR: Unable to extract text", file=sys.stderr)
        sys.exit(3)
    if names:
        print("\n".join(names))
    else:
        print("")

if __name__ == "__main__":
    main()
