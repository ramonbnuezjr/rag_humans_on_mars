"""Inventory, extract, index, and search local research evidence."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["inventory", "extract", "index", "search", "evaluate", "serve"])
    parser.add_argument("source_id", nargs="?", help="Registered source ID (except inventory)")
    parser.add_argument("question", nargs="?", help="Quoted search question")
    parser.add_argument("--top-k", type=int, default=5, help="Maximum passages returned (1-100)")
    parser.add_argument("--chunk-words", type=int, default=180, help="Index chunk size in words")
    parser.add_argument("--overlap-words", type=int, default=30, help="Index overlap in words")
    parser.add_argument("--parser", choices=["pypdf", "pdfplumber"], default="pypdf",
                        help="PDF extraction parser; pdfplumber uses reviewed geometric spacing settings")
    parser.add_argument("--ranking", choices=["baseline", "page", "context"], default="page",
                        help="baseline: original chunks; page: same ranking with page context (default); context: experimental query hints/page reranking")
    parser.add_argument("--eval-set", help="Dataset filename inside evals/ (evaluate all only)")
    parser.add_argument("--port", type=int, default=8765, help="Local UI port (serve only)")
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory)"
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "serve":
        if args.source_id or args.question or not 1 <= args.port <= 65535:
            parser.error("serve takes no source/question and requires a port from 1 to 65535.")
        from .web import serve
        try:
            serve(root, args.port)
        except OSError as error:
            parser.error("Cannot start the local UI: {}".format(error))
        return
    if args.command != "search" and args.question:
        parser.error("Only search takes a question argument.")
    if args.command in ("index", "search", "evaluate"):
        if not args.source_id:
            parser.error("{} requires a source ID.".format(args.command))
        try:
            if args.command == "index":
                from .index import build_index
                output, manifest = build_index(root, args.source_id, args.chunk_words, args.overlap_words)
                print("Local BM25 index ready: {}".format(args.source_id))
                print("Pages: {}; chunks: {}".format(manifest["page_count"], manifest["chunk_count"]))
                print("Output: {}".format(output.relative_to(root)))
                print("No embeddings, model calls, or network access. Original PDFs are unchanged.")
            elif args.command == "search":
                if not args.question:
                    parser.error("search requires a quoted question.")
                from .retrieve import search
                hits = search(root, args.source_id, args.question, args.top_k, ranking=args.ranking)
                print("Keyword matches in {}; these are passages, not generated answers.".format(
                    "all registered indexes" if args.source_id == "all" else args.source_id + " only"))
                if not hits:
                    print("No matching passages found. This does not prove the library lacks the information.")
                records = {s["source_id"]: s for s in json.loads(
                    (root / "sources/registry.json").read_text(encoding="utf-8"))["sources"]}
                shown = set()
                for number, hit in enumerate(hits, 1):
                    if hit["source_id"] not in shown:
                        source = records[hit["source_id"]]
                        print("\nSource context: {} | evidence: {} | metadata: {}".format(
                            source.get("mission_context", "not yet reviewed"),
                            source.get("evidence_type"), source.get("metadata_status")))
                        for limitation in source.get("extraction", {}).get("quality_limitations", []):
                            print("Review limitation: " + limitation)
                        shown.add(hit["source_id"])
                    print("\n{}. {} | PDF page {} | printed label {} | score {:.3f}".format(
                        number, hit["source_id"], hit["pdf_page_number"], hit["printed_page_label"], hit["score"]))
                    print("File: {}\nEdition: {}\nChunk: {}".format(hit["source_filename"], hit["source_edition"], hit["chunk_id"]))
                    print("PDF: {}#page={}".format(hit["source_local_path"], hit["pdf_page_number"]))
                    if "context_text" in hit:
                        print("Evidence: complete extracted PDF page | context ID: {}".format(hit["context_id"]))
                        print("Query hints: {}".format(", ".join(sorted(hit["query_expansions"])) or "none"))
                    print(hit.get("context_text", hit["text"]))
                print("\nKeyword scores are not confidence scores. Check assumptions, tables, and surrounding pages.")
            else:
                from .evaluate import evaluate
                if args.eval_set and args.source_id != "all":
                    parser.error("--eval-set requires evaluate all.")
                output, report = evaluate(root, args.source_id, args.top_k, ranking=args.ranking, dataset_path=args.eval_set)
                print("Retrieval development checks: {}/{} passed at top-{}.".format(report["passed"], report["total"], args.top_k))
                for case in report["results"]:
                    label = "REVIEW" if case["passed"] is None else "PASS" if case["passed"] else "FAIL"
                    print("{} {} | returned pages {}".format(label, case["id"], case["returned_pages"]))
                if "manual_gap_cases" in report:
                    print("Unscored gap questions requiring review: {}".format(report["manual_gap_cases"]))
                print("Report: {}".format(output.relative_to(root)))
                print(report["limitations"])
                if report["passed"] != report["total"]:
                    parser.exit(1)
        except (OSError, ValueError, KeyError) as error:
            parser.error(str(error))
        return
    if args.command == "extract":
        if not args.source_id:
            parser.error("extract requires a source ID, e.g. extract mars-007")
        from .ingest import extract_source
        try:
                output, manifest = extract_source(root, args.source_id, parser=args.parser)
        except (OSError, ValueError, KeyError) as error:
            parser.error(str(error))
        print("Page-preserving extraction ready: {}".format(args.source_id))
        print("Pages: {}; empty text pages: {}".format(manifest["page_count"], manifest["empty_text_pages"]))
        print("Output: {}".format(output.relative_to(root)))
        print("Text only; tables, figures, equations, and reading order require review.")
        return
    if args.source_id:
        parser.error("inventory does not take a source ID")
    registry_path = root / "sources" / "registry.json"
    if not registry_path.is_file():
        parser.error("Source register not found. Run from the repository root or pass --root.")
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.error("Cannot read source register: {}".format(error))
    raw = root / "data" / "raw"
    pdfs = {path.relative_to(root).as_posix() for path in raw.rglob("*")
            if path.is_file() and path.suffix.lower() == ".pdf"}
    registered = {source["local_path"] for source in registry["sources"]}
    print("Humans on Mars — collection inventory")
    print("Stage: local extraction, indexing, and keyword retrieval available; answer generation is not implemented.")
    print("Local PDFs: {}".format(len(pdfs)))
    print("Registered sources: {}".format(len(registered)))
    print("Sources marked indexed: {} (index integrity not checked by inventory)".format(sum(
        bool(source.get("index")) for source in registry["sources"])))
    print("Sources pending metadata review: {}".format(sum(
        source["metadata_status"] != "verified" for source in registry["sources"])))
    print("PDF contents and hashes are not verified by this command.")
    for path in sorted(registered - pdfs):
        print("Missing locally: {}".format(path))
    for path in sorted(pdfs - registered):
        print("Unregistered PDF: {}".format(path))
