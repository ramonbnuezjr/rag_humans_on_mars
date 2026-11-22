"""Small source-specific retrieval checks, separate from answer generation."""

import json
from pathlib import Path

from .index import digest, json_bytes, load_index
from .retrieve import search
from .retrieve import indexed_source_ids
from .ranking import RANKING_VERSION, SETTINGS, CONCEPTS, TITLE_HINTS


def ranking_record(ranking):
    return {"method": {"baseline": "bm25-v1", "page": "page-v1", "context": RANKING_VERSION}[ranking],
            "evidence_unit": "anchor_chunk" if ranking == "baseline" else "parent_pdf_page",
            "configuration_sha256": digest(json_bytes([SETTINGS, CONCEPTS, sorted(TITLE_HINTS)])) if ranking == "context" else None}


def evaluate(root, source_id, top_k=5, ranking="page", dataset_path=None):
    if source_id == "all":
        return evaluate_research(root, combined=True, top_k=top_k, ranking=ranking, dataset_path=dataset_path)
    root = Path(root).resolve()
    manifest, _ = load_index(root, source_id)
    path = root / "evals" / (source_id + "-retrieval.jsonl")
    content = path.read_bytes()
    cases = [json.loads(line) for line in content.decode("utf-8").splitlines() if line.strip()]
    if not cases:
        raise ValueError("Evaluation set is empty.")
    results = []
    for case in cases:
        if case["source_id"] != source_id or case["source_sha256"] != manifest["source_sha256"]:
            raise ValueError("Evaluation cases do not match this indexed source version.")
        hits = search(root, source_id, case["question"], top_k, ranking=ranking)
        support_rank = None
        if case.get("lexical_no_match_probe"):
            passed = not hits
        else:
            ranks = [rank for rank, hit in enumerate(hits, 1)
                     if hit["pdf_page_number"] in case["expected_pages"]
                     and all(term.casefold() in " ".join(hit.get("context_text", hit["text"]).casefold().split())
                             for term in case["expected_contains"])]
            support_rank = ranks[0] if ranks else None
            passed = support_rank is not None
        results.append({"id": case["id"], "question": case["question"], "passed": passed,
                        "support_rank": support_rank,
                        "lexical_no_match_probe": case.get("lexical_no_match_probe", False),
                        "returned_pages": [h["pdf_page_number"] for h in hits],
                        "chunk_ids": [h["chunk_id"] for h in hits], "expected_pages": case["expected_pages"]})
    evidence_cases = [r for r in results if not r["lexical_no_match_probe"]]
    report = {"schema_version": 1, "source_id": source_id, "index_id": manifest["index_id"],
              "evaluation_sha256": digest(content), "top_k": top_k, "ranking": ranking_record(ranking),
              "evidence_cases": len(evidence_cases),
              "evidence_hits_at_k": sum(r["passed"] for r in evidence_cases),
              "evidence_hits_at_1": sum(r["support_rank"] == 1 for r in evidence_cases),
              "mean_reciprocal_rank_at_k": (sum(1 / r["support_rank"] if r["support_rank"] else 0
                                                 for r in evidence_cases) / len(evidence_cases)) if evidence_cases else None,
              "passed": sum(r["passed"] for r in results), "total": len(results), "results": results,
              "limitations": "Provisional agent-reviewed development cases, not a held-out benchmark or answer-quality evaluation. A no-match probe only tests keyword behavior."}
    output = root / "evals/results" / (source_id + "-" + digest(json_bytes(report)) + ".json")
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json_bytes(report)
    if output.exists() and output.read_bytes() != encoded:
        raise ValueError("Evaluation output conflict; refusing to overwrite.")
    if not output.exists():
        output.write_bytes(encoded)
    return output, report


def evaluate_research(root, combined=False, top_k=5, ranking="page", dataset_path=None):
    """Draft question checks; gap labels require review, never automatic abstention.

    Source mode tests each expected source independently; combined mode requires
    retrieval to select the right source too. Record all active index identities.
    """
    root = Path(root).resolve()
    path = (root / "evals" / (dataset_path or "research-retrieval.jsonl")).resolve()
    if (root / "evals").resolve() not in path.parents:
        raise ValueError("Evaluation dataset must remain inside evals/.")
    content = path.read_bytes()
    cases = [json.loads(line) for line in content.decode("utf-8").splitlines() if line.strip()]
    if not cases:
        raise ValueError("Evaluation set is empty.")
    manifests = {sid: load_index(root, sid)[0] for sid in indexed_source_ids(root)}
    results = []
    for case in cases:
        sid = case.get("expected_source_id")
        if sid and sid not in manifests:
            raise ValueError("Expected source is not indexed: {}".format(sid))
        if sid and case.get("source_sha256") and case["source_sha256"] != manifests[sid]["source_sha256"]:
            raise ValueError("Evaluation case differs from indexed source version.")
        hits = search(root, "all" if combined or not sid else sid, case["question"], top_k, ranking=ranking)
        ranks = [rank for rank, hit in enumerate(hits, 1)
                 if hit["source_id"] == sid and hit["pdf_page_number"] in case.get("expected_pages", [])
                 and all(term.casefold() in " ".join(hit.get("context_text", hit["text"]).casefold().split())
                         for term in case.get("expected_contains", []))]
        anchor_ranks = [rank for rank, hit in enumerate(hits, 1)
                        if hit["source_id"] == sid and hit["pdf_page_number"] in case.get("expected_pages", [])
                        and all(term.casefold() in " ".join(hit["text"].casefold().split())
                                for term in case.get("expected_contains", []))]
        results.append({"id": case["id"], "question": case["question"],
                        "evidence_status": case["evidence_status"],
                        "answer_boundary": case["answer_boundary"],
                        "passed": bool(ranks) if sid else None,
                        "support_rank": ranks[0] if ranks else None,
                        "anchor_support_rank": anchor_ranks[0] if anchor_ranks else None,
                        "returned_pages": [h["pdf_page_number"] for h in hits],
                        "returned_sources": [h["source_id"] for h in hits],
                        "chunk_ids": [h["chunk_id"] for h in hits],
                        "context_ids": [h.get("context_id") for h in hits]})
    scored = [r for r in results if r["passed"] is not None]
    report = {"schema_version": 1, "mode": "combined" if combined else "source_scoped",
              "index_ids": {sid: m["index_id"] for sid, m in manifests.items()},
              "source_hashes": {sid: m["source_sha256"] for sid, m in manifests.items()},
              "evaluation_sha256": digest(content), "top_k": top_k,
              "dataset_path": str(path.relative_to(root)), "ranking": ranking_record(ranking),
              "passed": sum(r["passed"] for r in scored), "total": len(scored),
              "anchor_hits_at_k": sum(r["anchor_support_rank"] is not None for r in scored),
              "evidence_hits_at_1": sum(r["support_rank"] == 1 for r in scored),
              "manual_gap_cases": len(results) - len(scored), "results": results,
              "limitations": "Draft agent-reviewed development questions, not held-out or answer-quality evaluation. Partial cases check relevant evidence location only. Gap cases are unscored: retrieval does not classify sufficiency or abstain. Historical reports and different mission concepts require attribution."}
    output = root / "evals/results" / ("research-" + report["mode"] + "-" + digest(json_bytes(report)) + ".json")
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json_bytes(report)
    if output.exists() and output.read_bytes() != encoded:
        raise ValueError("Evaluation output conflict; refusing to overwrite.")
    if not output.exists():
        output.write_bytes(encoded)
    return output, report
