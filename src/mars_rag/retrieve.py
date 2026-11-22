"""Rank local evidence passages; no model, embeddings, or network calls."""

import math
import json
from pathlib import Path
from collections import Counter, defaultdict

from .index import load_index, load_extraction, tokenize, digest, json_bytes
from .ranking import query_weights, TITLE_HINTS, SETTINGS, RANKING_VERSION


def search(root, source_id, question, top_k=5, ranking="page"):
    if not 1 <= top_k <= 100:
        raise ValueError("top_k must be between 1 and 100.")
    terms = set(tokenize(question))
    if not terms:
        raise ValueError("Question must contain searchable terms.")
    if ranking not in ("baseline", "page", "context"):
        raise ValueError("Unknown ranking method.")
    if ranking != "baseline":
        return _search_context(root, source_id, question, top_k, rerank=ranking == "context")
    if source_id == "all":
        return search_all(root, question, top_k)
    manifest, index = load_index(root, source_id)
    return [{**index["chunks"][n], "score": score, "index_id": manifest["index_id"]}
            for n, score in _rank(index, manifest["settings"], terms, top_k)]


def _rank(index, settings, terms, top_k):
    count = len(index["chunks"])
    average = sum(index["lengths"]) / count
    k1, b = settings["k1"], settings["b"]
    scores = {}
    for term in sorted(terms):
        matches = index["postings"].get(term, [])
        weight = terms[term] if isinstance(terms, dict) else 1.0
        idf = weight * math.log(1 + (count - len(matches) + 0.5) / (len(matches) + 0.5))
        for number, frequency in matches:
            denominator = frequency + k1 * (1 - b + b * index["lengths"][number] / average)
            scores[number] = scores.get(number, 0) + idf * frequency * (k1 + 1) / denominator
    ranked = sorted(scores, key=lambda n: (-scores[n], n))[:top_k]
    return [(n, scores[n]) for n in ranked]


def indexed_source_ids(root):
    registry = json.loads((Path(root) / "sources/registry.json").read_text(encoding="utf-8"))
    ids = sorted(s["source_id"] for s in registry["sources"] if s.get("index"))
    if not ids:
        raise ValueError("No registered indexes available.")
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate source IDs in register.")
    return ids


def search_all(root, question, top_k=5):
    """Rank a verified union using corpus-wide BM25 statistics, not mixed scores.

    Unindexed sources are excluded. A stale/corrupt included index fails the whole
    search, rather than silently returning an incomplete collection.
    """
    if not 1 <= top_k <= 100:
        raise ValueError("top_k must be between 1 and 100.")
    terms = set(tokenize(question))
    if not terms:
        raise ValueError("Question must contain searchable terms.")
    union = {"chunks": [], "lengths": [], "postings": {}}
    settings = None
    for sid in indexed_source_ids(root):
        manifest, index = load_index(root, sid)
        if settings is not None and settings != manifest["settings"]:
            raise ValueError("Included indexes have incompatible ranking/chunk settings.")
        settings = manifest["settings"]
        offset = len(union["chunks"])
        union["chunks"].extend({**c, "index_id": manifest["index_id"]} for c in index["chunks"])
        union["lengths"].extend(index["lengths"])
        for term, postings in index["postings"].items():
            union["postings"].setdefault(term, []).extend([n + offset, f] for n, f in postings)
    return [{**union["chunks"][n], "score": score}
            for n, score in _rank(union, settings, terms, top_k)]


def _search_context(root, source_id, question, top_k, rerank=True):
    """Score anchors and complete parent pages, returning diverse page contexts.

    Original chunks remain exact/unchanged. Context is verified extracted page
    text with its own ID and full-page offsets, never inferred neighboring text.
    """
    ids = indexed_source_ids(root) if source_id == "all" else [source_id]
    union = {"chunks": [], "lengths": [], "postings": {}}
    parents = {"chunks": [], "lengths": [], "postings": defaultdict(list)}
    page_lookup = {}
    settings = None
    for sid in ids:
        manifest, index = load_index(root, sid)
        if settings is not None and settings != manifest["settings"]:
            raise ValueError("Included indexes have incompatible ranking/chunk settings.")
        settings = manifest["settings"]
        _, _, extraction, pages = load_extraction(root, sid)
        if extraction["extraction_id"] != manifest["extraction_id"]:
            raise ValueError("Extraction changed while loading search context.")
        for page in pages:
            if not page["text"].strip():
                continue
            number = len(parents["chunks"])
            page_lookup[sid, page["pdf_page_number"]] = number
            parents["chunks"].append(page)
            counts = Counter(tokenize(page["text"]))
            parents["lengths"].append(sum(counts.values()))
            for term, frequency in counts.items():
                parents["postings"][term].append([number, frequency])
        offset = len(union["chunks"])
        union["chunks"].extend({**c, "index_id": manifest["index_id"]} for c in index["chunks"])
        union["lengths"].extend(index["lengths"])
        for term, postings in index["postings"].items():
            union["postings"].setdefault(term, []).extend([n + offset, f] for n, f in postings)
    weights = query_weights(question) if rerank else {term: 1.0 for term in tokenize(question)}
    page_scores = dict(_rank(parents, settings, weights, len(parents["chunks"])))
    anchors = _rank(union, settings, weights, len(union["chunks"]))
    candidates = []
    for number, anchor_score in anchors:
        chunk = union["chunks"][number]
        parent_number = page_lookup[chunk["source_id"], chunk["pdf_page_number"]]
        title_terms = set(tokenize(chunk.get("source_title") or ""))
        boost = 1 + SETTINGS["title_hint_boost"] * len(set(weights) & TITLE_HINTS & title_terms)
        score = (anchor_score + SETTINGS["page_weight"] * page_scores.get(parent_number, 0)) * boost if rerank else anchor_score
        candidates.append((score, number, parent_number))
    seen = set()
    hits = []
    for score, number, parent_number in sorted(candidates, key=lambda c: (-c[0], c[1])):
        if rerank and parent_number in seen:
            continue
        seen.add(parent_number)
        chunk = union["chunks"][number]
        page = parents["chunks"][parent_number]
        context_id = digest(json_bytes([chunk["source_sha256"], chunk["extraction_id"],
                                        page["pdf_page_number"], page["text"]]))
        hits.append({**chunk, "score": score, "ranking_method": RANKING_VERSION if rerank else "page-v1",
                     "query_expansions": {t: w for t, w in weights.items() if w != 1},
                     "context_text": page["text"], "context_id": context_id,
                     "context_char_start": 0, "context_char_end": len(page["text"])})
        if len(hits) == top_k:
            break
    return hits
