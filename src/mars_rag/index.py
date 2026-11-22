"""Build an immutable local BM25 index from a verified page extraction."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile


INDEXER_VERSION = "1"
STOP_WORDS = frozenset("a an and are as at be by can do does for from how i in is it of on or that the these this to was what when which who why with would".split())


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def digest(content):
    return hashlib.sha256(content).hexdigest()


def tokenize(text):
    """Version-1 tokenizer: lowercase alphanumerics, fixed stop list, no stemming."""
    return [term for term in re.findall(r"[a-z0-9]+", text.casefold()) if term not in STOP_WORDS]


def source_record(root, source_id):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", source_id):
        raise ValueError("Invalid source ID.")
    register = json.loads((root / "sources/registry.json").read_text(encoding="utf-8"))
    matches = [s for s in register["sources"] if s["source_id"] == source_id]
    if len(matches) != 1:
        raise ValueError("Expected exactly one registered source: {}".format(source_id))
    return register, matches[0]


def inside(root, relative, folder):
    path = (root / relative).resolve()
    if root / folder not in path.parents:
        raise ValueError("Path must remain inside {}.".format(folder))
    return path


def load_extraction(root, source_id):
    """Reject altered originals, stale source metadata, or changed extraction files."""
    root = Path(root).resolve()
    register, source = source_record(root, source_id)
    original = inside(root, source["local_path"], "data/raw")
    if digest(original.read_bytes()) != source["sha256"]:
        raise ValueError("Original PDF hash changed; review and re-extract before indexing.")
    if not source.get("extraction"):
        raise ValueError("Source has no registered extraction; run extract first.")
    path = inside(root, source["extraction"]["manifest_path"], "data/processed")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if (manifest["source_id"] != source_id or manifest["source_sha256"] != source["sha256"]
            or manifest["extraction_id"] != source["extraction"]["extraction_id"]):
        raise ValueError("Extraction provenance differs from the source register.")
    content = (path.parent / "pages.jsonl").read_bytes()
    if digest(content) != manifest["pages_sha256"]:
        raise ValueError("Extracted page checksum mismatch.")
    pages = [json.loads(line) for line in content.decode("utf-8").splitlines()]
    if [p["pdf_page_number"] for p in pages] != list(range(1, manifest["page_count"] + 1)):
        raise ValueError("Extraction must contain one ordered record per PDF page.")
    expected = {"source_id": source_id, "source_sha256": source["sha256"],
                "source_filename": source["filename"], "source_local_path": source["local_path"],
                "source_title": source.get("title"), "source_edition": source.get("edition"),
                "source_url": source.get("canonical_url")}
    for page in pages:
        if any(page.get(k) != v for k, v in expected.items()):
            raise ValueError("Source metadata changed; rerun extract before indexing.")
        if page.get("printed_page_label") != source.get("printed_page_labels", {}).get(str(page["pdf_page_number"])):
            raise ValueError("Reviewed page labels changed; rerun extract before indexing.")
    return register, source, manifest, pages


def chunk_pages(pages, extraction_id, chunk_words=180, overlap_words=30):
    """Page-bounded raw-text slices with exact offsets and reproducible IDs."""
    if chunk_words < 1 or overlap_words < 0 or overlap_words >= chunk_words:
        raise ValueError("Require chunk_words > overlap_words >= 0.")
    chunks = []
    for page in pages:
        words = list(re.finditer(r"\S+", page["text"]))
        for start in range(0, len(words), chunk_words - overlap_words):
            end = min(start + chunk_words, len(words))
            char_start, char_end = words[start].start(), words[end - 1].end()
            text = page["text"][char_start:char_end]
            identity = [page["source_sha256"], extraction_id, page["pdf_page_number"], char_start, char_end, digest(text.encode("utf-8"))]
            chunks.append({**{k: v for k, v in page.items() if k not in ("text", "schema_version")},
                           "chunk_id": digest(json_bytes(identity)), "extraction_id": extraction_id,
                           "pdf_page_start": page["pdf_page_number"], "pdf_page_end": page["pdf_page_number"],
                           "char_start": char_start, "char_end": char_end, "text": text})
            if end == len(words):
                break
    return chunks


def build_index(root, source_id, chunk_words=180, overlap_words=30):
    root = Path(root).resolve()
    register, source, extraction, pages = load_extraction(root, source_id)
    chunks = chunk_pages(pages, extraction["extraction_id"], chunk_words, overlap_words)
    if not chunks:
        raise ValueError("No extractable text to index; OCR or source review is needed.")
    postings = defaultdict(list)
    lengths = []
    for number, chunk in enumerate(chunks):
        counts = Counter(tokenize(chunk["text"]))
        lengths.append(sum(counts.values()))
        for term, frequency in sorted(counts.items()):
            postings[term].append([number, frequency])
    if not postings:
        raise ValueError("No searchable terms to index.")
    payload = {"chunks": chunks, "postings": dict(postings), "lengths": lengths}
    payload_bytes = json_bytes(payload)
    settings = {"method": "BM25", "chunk_words": chunk_words, "overlap_words": overlap_words,
                "page_bounded": True, "tokenizer_version": "1", "stop_words": sorted(STOP_WORDS),
                "stemming": False, "k1": 1.2, "b": 0.75, "embeddings": None}
    identity = {"indexer_version": INDEXER_VERSION, "source_id": source_id, "source_sha256": source["sha256"],
                "extraction_id": extraction["extraction_id"], "pages_sha256": extraction["pages_sha256"],
                "settings": settings, "index_sha256": digest(payload_bytes)}
    index_id = digest(json_bytes(identity))
    manifest = {"schema_version": 1, "index_id": index_id, **identity, "page_count": len(pages),
                "chunk_count": len(chunks), "limitations": extraction["limitations"] + [
                    "Keyword ranking is not semantic search or answerability validation.",
                    "Chunks do not cross pages; inspect adjacent pages for continued arguments."]}
    output = root / "data/index" / source_id / index_id
    inside(root, output.relative_to(root), "data/index")
    expected = {"index.json": payload_bytes, "manifest.json": json_bytes(manifest)}
    if output.exists():
        if any(not (output / name).is_file() or (output / name).read_bytes() != content
               for name, content in expected.items()):
            raise ValueError("Existing index differs; refusing to overwrite: {}".format(output))
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".index-", dir=output.parent))
        try:
            for name, content in expected.items():
                (staging / name).write_bytes(content)
            staging.rename(output)
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    source["indexing_status"] = "indexed_local_bm25"
    source["index"] = {"index_id": index_id, "manifest_path": (output / "manifest.json").relative_to(root).as_posix()}
    register_path = root / "sources/registry.json"
    new_register = (json.dumps(register, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if register_path.read_bytes() != new_register:
        register_path.write_bytes(new_register)
    return output, manifest


def load_index(root, source_id):
    root = Path(root).resolve()
    _, source, extraction, _ = load_extraction(root, source_id)
    if not source.get("index"):
        raise ValueError("Source has no index; run index first.")
    path = inside(root, source["index"]["manifest_path"], "data/index")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if (manifest["index_id"] != source["index"]["index_id"] or manifest["source_id"] != source_id
            or manifest["source_sha256"] != source["sha256"] or manifest["extraction_id"] != extraction["extraction_id"]
            or manifest["pages_sha256"] != extraction["pages_sha256"]):
        raise ValueError("Index is stale; rebuild it from the current extraction.")
    if manifest["indexer_version"] != INDEXER_VERSION:
        raise ValueError("Index version is unsupported; rebuild the index.")
    content = (path.parent / "index.json").read_bytes()
    if digest(content) != manifest["index_sha256"]:
        raise ValueError("Index checksum mismatch; existing output was not replaced.")
    return manifest, json.loads(content)
