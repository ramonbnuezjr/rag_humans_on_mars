"""Local text extraction with one provenance-bearing record per PDF page."""

import hashlib
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import tempfile


EXTRACTOR_VERSION = "1"
LIMITATIONS = [
    "Text only: tables, equations, plots, images, and reading order need review.",
    "No OCR: empty pages are retained and flagged, not silently discarded.",
    "Extracted source text is untrusted evidence, never application instructions.",
]


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def extract_source(root, source_id, parser="pypdf"):
    """Extract a registered PDF; verify its hash and never replace prior output.

    Returns the output directory and manifest. An identical rerun reuses verified
    output. Source/metadata/parser changes create a separate output directory.
    """
    # Inventory remains usable without the optional PDF dependency.
    try:
        import pypdf
    except ImportError as error:
        raise ValueError("Install extraction support: python -m pip install -e '.[extraction]'") from error

    if parser not in ("pypdf", "pdfplumber"):
        raise ValueError("Unsupported PDF parser.")
    root = Path(root).resolve()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", source_id):
        raise ValueError("Source ID must contain only letters, numbers, underscores, or hyphens.")
    registry = json.loads((root / "sources/registry.json").read_text(encoding="utf-8"))
    matches = [s for s in registry["sources"] if s["source_id"] == source_id]
    if len(matches) != 1:
        raise ValueError("Expected one registered source for {!r}; found {}.".format(source_id, len(matches)))
    source = matches[0]
    source_path = (root / source["local_path"]).resolve()
    raw = root / "data/raw"
    if raw not in source_path.parents or source_path.suffix.lower() != ".pdf":
        raise ValueError("Source must be a PDF inside data/raw/.")
    source_bytes = source_path.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    if source_hash != source["sha256"]:
        raise ValueError("Source SHA-256 differs from the register; no output written.")

    try:
        reader = pypdf.PdfReader(BytesIO(source_bytes))
    except pypdf.errors.PyPdfError as error:
        raise ValueError("Cannot read PDF: {}".format(error)) from error
    if reader.is_encrypted:
        raise ValueError("Encrypted PDFs are not supported by this extraction command.")
    if not reader.pages:
        raise ValueError("PDF contains no pages.")

    # Printed labels are manually reviewed metadata, never inferred from position.
    printed_labels = source.get("printed_page_labels", {})
    if not isinstance(printed_labels, dict):
        raise ValueError("printed_page_labels must map one-based PDF positions to reviewed labels.")
    valid_positions = {str(n) for n in range(1, len(reader.pages) + 1)}
    for position, label in printed_labels.items():
        if position not in valid_positions or not isinstance(label, str) or not label:
            raise ValueError("Invalid reviewed printed-page label.")
    embedded_labels = reader.page_labels if "/PageLabels" in reader.trailer["/Root"] else None
    settings = {"extraction_mode": "plain", "ocr": False, "text_normalization": "none"}
    parser_version = pypdf.__version__
    if parser == "pdfplumber":
        try:
            import pdfplumber
        except ImportError as error:
            raise ValueError("Install spacing support: python -m pip install -e '.[extraction_spacing]'") from error
        settings = {"layout": False, "x_tolerance": 1, "y_tolerance": 3,
                    "ocr": False, "text_normalization": "none",
                    "pdfminer_version": version("pdfminer.six"),
                    "page_label_parser": "pypdf", "page_label_parser_version": pypdf.__version__}
        parser_version = pdfplumber.__version__
        with pdfplumber.open(BytesIO(source_bytes)) as document:
            if len(document.pages) != len(reader.pages):
                raise ValueError("PDF parsers disagree on page count.")
            texts = [page.extract_text(layout=False, x_tolerance=1, y_tolerance=3) or ""
                     for page in document.pages]
    else:
        texts = [page.extract_text(extraction_mode="plain") or "" for page in reader.pages]
    records = []
    for number, text in enumerate(texts, 1):
        records.append({
            "schema_version": 1,
            "source_id": source_id,
            "source_sha256": source_hash,
            "source_filename": source["filename"],
            "source_local_path": source["local_path"],
            "source_title": source.get("title"),
            "source_edition": source.get("edition"),
            "source_url": source.get("canonical_url"),
            "pdf_page_number": number,
            "pdf_page_label": embedded_labels[number - 1] if embedded_labels else None,
            "printed_page_label": printed_labels.get(str(number)),
            "text": text,
            "warnings": [] if text.strip() else ["no_extractable_text"],
        })
    pages_bytes = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    provenance = {
        "extractor_version": EXTRACTOR_VERSION,
        "parser": parser,
        "parser_version": parser_version,
        "settings": settings,
        "source_id": source_id,
        "source_sha256": source_hash,
        "page_metadata_sha256": hashlib.sha256(_json_bytes([
            {k: v for k, v in r.items() if k not in ("text", "warnings")} for r in records
        ])).hexdigest(),
    }
    run_id = hashlib.sha256(_json_bytes(provenance)).hexdigest()
    manifest = {
        "schema_version": 1,
        "extraction_id": run_id,
        **provenance,
        "page_count": len(records),
        "empty_text_pages": [r["pdf_page_number"] for r in records if r["warnings"]],
        "pages_file": "pages.jsonl",
        "pages_sha256": hashlib.sha256(pages_bytes).hexdigest(),
        "limitations": LIMITATIONS,
    }
    processed = root / "data/processed"
    output = processed / source_id / source_hash / run_id
    if processed not in output.resolve().parents:
        raise ValueError("Extraction output must remain inside data/processed/.")
    expected = {"pages.jsonl": pages_bytes, "manifest.json": _json_bytes(manifest)}
    if output.exists():
        if any(not (output / name).is_file() or (output / name).read_bytes() != content
               for name, content in expected.items()):
            raise ValueError("Existing extraction differs; refusing to overwrite: {}".format(output))
        return output, manifest

    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".extract-", dir=output.parent))
    try:
        for name, content in expected.items():
            (staging / name).write_bytes(content)
        staging.rename(output)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return output, manifest
