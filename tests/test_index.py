"""Small end-to-end checks for local indexing, ranking, and provenance."""

import contextlib
import io
import json
import hashlib
import math
from pathlib import Path
import unittest
from unittest.mock import patch

import test_ingest
from mars_rag.cli import main
from mars_rag.evaluate import evaluate, evaluate_research
from mars_rag.index import build_index, chunk_pages, load_index
from mars_rag.ingest import extract_source
from mars_rag.retrieve import search
from mars_rag.ranking import query_weights


class IndexTests(unittest.TestCase):
    def setUp(self):
        fixture = test_ingest.ExtractionTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.prepare()
        self.root = fixture.root.resolve()
        output, manifest = extract_source(self.root, "example")
        path = self.root / "sources/registry.json"
        register = json.loads(path.read_text())
        register["sources"][0]["extraction"] = {
            "extraction_id": manifest["extraction_id"],
            "manifest_path": (output / "manifest.json").relative_to(self.root).as_posix()}
        path.write_text(json.dumps(register))
        self.pages_path = output / "pages.jsonl"

    def test_chunk_boundaries_exact_offsets_overlap_and_metadata(self):
        page = json.loads(self.pages_path.read_text().splitlines()[0])
        page["text"] = "one  two\nthree four five six seven"
        chunks = chunk_pages([page], "extract-id", 4, 1)
        self.assertEqual([c["text"] for c in chunks], ["one  two\nthree four", "four five six seven"])
        for chunk in chunks:
            self.assertEqual(chunk["text"], page["text"][chunk["char_start"]:chunk["char_end"]])
            self.assertEqual(chunk["source_edition"], "reviewed v2")
            self.assertEqual(chunk["printed_page_label"], "A-1")
            self.assertEqual(chunk["pdf_page_start"], chunk["pdf_page_end"])
        self.assertEqual(chunks, chunk_pages([page], "extract-id", 4, 1))
        with self.assertRaises(ValueError):
            chunk_pages([page], "extract-id", 3, 3)

    def test_index_search_and_no_match(self):
        original = (self.root / "data/raw/example.pdf").read_bytes()
        output, manifest = build_index(self.root, "example")
        self.assertEqual(manifest["chunk_count"], 2)
        hits = search(self.root, "example", "second", 1)
        self.assertEqual(hits[0]["pdf_page_number"], 2)
        self.assertIn("Second page evidence", hits[0]["text"])
        self.assertEqual(hits[0]["source_edition"], "reviewed v2")
        self.assertEqual(search(self.root, "example", "platypus"), [])
        for question, top_k in [("the and", 5), ("second", 0)]:
            with self.assertRaises(ValueError):
                search(self.root, "example", question, top_k)
        self.assertEqual((self.root / "data/raw/example.pdf").read_bytes(), original)
        self.assertTrue((output / "index.json").exists())

    def test_reruns_and_corrupted_index_preservation(self):
        output, _ = build_index(self.root, "example")
        path = output / "index.json"
        stamp = path.stat().st_mtime_ns
        self.assertEqual(build_index(self.root, "example")[0], output)
        self.assertEqual(path.stat().st_mtime_ns, stamp)
        path.write_text("corrupted")
        with self.assertRaisesRegex(ValueError, "checksum"):
            load_index(self.root, "example")
        with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
            build_index(self.root, "example")
        self.assertEqual(path.read_text(), "corrupted")

    def test_changed_extraction_and_metadata_are_rejected(self):
        build_index(self.root, "example")
        original = self.pages_path.read_bytes()
        self.pages_path.write_bytes(original + b"changed")
        with self.assertRaisesRegex(ValueError, "checksum"):
            search(self.root, "example", "second")
        self.pages_path.write_bytes(original)
        register_path = self.root / "sources/registry.json"
        register = json.loads(register_path.read_text())
        register["sources"][0]["edition"] = "new edition"
        register_path.write_text(json.dumps(register))
        with self.assertRaisesRegex(ValueError, "metadata changed"):
            search(self.root, "example", "second")

    def test_original_hash_is_checked(self):
        original = self.root / "data/raw/example.pdf"
        original.write_bytes(original.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "hash changed"):
            build_index(self.root, "example")
        self.assertFalse((self.root / "data/index").exists())

    def add_second_source(self):
        path = self.root / "sources/registry.json"
        reg = json.loads(path.read_text())
        source = dict(reg["sources"][0])
        source.pop("extraction", None)
        source.pop("index", None)
        source.update(source_id="other", filename="other.pdf", local_path="data/raw/other.pdf")
        raw = (self.root / "data/raw/example.pdf").read_bytes().replace(b"Second page evidence", b"Fourth page evidence")
        (self.root / source["local_path"]).write_bytes(raw)
        source["sha256"] = hashlib.sha256(raw).hexdigest()
        reg["sources"].append(source)
        path.write_text(json.dumps(reg))
        out, m = extract_source(self.root, "other")
        source["extraction"] = {"extraction_id": m["extraction_id"],
                                "manifest_path": (out / "manifest.json").relative_to(self.root).as_posix()}
        path.write_text(json.dumps(reg))

    def test_combined_search_global_statistics_and_provenance(self):
        build_index(self.root, "example")
        self.add_second_source()
        self.assertEqual(len(search(self.root, "all", "evidence")), 2)  # unindexed excluded
        build_index(self.root, "other")
        hits = search(self.root, "all", "second")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["source_id"], "example")
        self.assertEqual(hits[0]["pdf_page_number"], 2)
        self.assertAlmostEqual(hits[0]["score"], math.log(1 + 3.5 / 1.5))
        all_hits = search(self.root, "all", "evidence")
        self.assertEqual({h["source_id"] for h in all_hits}, {"example", "other"})
        self.assertTrue(all(h["index_id"] and h["chunk_id"] for h in all_hits))
        self.assertEqual(search(self.root, "all", "platypus"), [])
        self.assertEqual(all_hits, search(self.root, "all", "evidence"))
        output = io.StringIO()
        with patch("sys.argv", ["mars-rag", "search", "all", "second", "--root", str(self.root)]), contextlib.redirect_stdout(output):
            main()
        self.assertIn("all registered indexes", output.getvalue())

    def test_combined_search_fails_on_stale_included_source(self):
        build_index(self.root, "example")
        self.add_second_source()
        out, _ = build_index(self.root, "other")
        (out / "index.json").write_text("changed")
        with self.assertRaisesRegex(ValueError, "checksum"):
            search(self.root, "all", "second")

    def test_parent_context_exactness_and_baseline_ranking_preserved(self):
        build_index(self.root, "example", chunk_words=2, overlap_words=1)
        baseline = search(self.root, "all", "page", ranking="baseline")
        pages = search(self.root, "all", "page", ranking="page")
        self.assertEqual([(h["chunk_id"], h["score"]) for h in baseline],
                         [(h["chunk_id"], h["score"]) for h in pages])
        originals = [json.loads(x) for x in self.pages_path.read_text().splitlines()]
        for hit in pages:
            original = originals[hit["pdf_page_number"] - 1]["text"]
            self.assertEqual(hit["context_text"], original)
            self.assertEqual(hit["context_char_start"], 0)
            self.assertEqual(hit["context_char_end"], len(original))
            self.assertEqual(hit["text"], original[hit["char_start"]:hit["char_end"]])
            self.assertTrue(hit["context_id"])
        self.assertEqual(pages, search(self.root, "all", "page"))

    def test_context_ranking_returns_unique_pages_without_changing_index(self):
        out, _ = build_index(self.root, "example", chunk_words=2, overlap_words=1)
        before = (out / "index.json").read_bytes()
        hits = search(self.root, "all", "page", ranking="context")
        self.assertEqual(len(hits), 2)
        self.assertEqual(len({(h["source_id"], h["pdf_page_number"]) for h in hits}), 2)
        self.assertTrue(all(h["ranking_method"] == "context-v1" for h in hits))
        self.assertEqual((out / "index.json").read_bytes(), before)
        with self.assertRaisesRegex(ValueError, "Unknown ranking"):
            search(self.root, "all", "page", ranking="unknown")

    def test_query_hints_are_explicit_and_phrase_bounded(self):
        weights = query_weights("How does weightlessness affect fitness?")
        self.assertEqual(weights["weightlessness"], 1)
        self.assertEqual(weights["microgravity"], 0.5)
        self.assertEqual(weights["rehabilitation"], 0.5)
        self.assertNotIn("microgravity", query_weights("weightlessnesses"))
        self.assertIn("eclss", query_weights("life-support equipment"))

    def test_evaluation_separates_anchor_hits_from_page_context(self):
        build_index(self.root, "example", chunk_words=2, overlap_words=1)
        source = json.loads((self.root / "sources/registry.json").read_text())["sources"][0]
        case = {"id": "split", "question": "first", "expected_source_id": "example",
                "source_sha256": source["sha256"], "expected_pages": [1],
                "expected_contains": ["evidence"], "evidence_status": "partial", "answer_boundary": "partial"}
        path = self.root / "evals/research-retrieval.jsonl"
        path.parent.mkdir()
        path.write_text(json.dumps(case) + "\n")
        _, baseline = evaluate_research(self.root, combined=True, ranking="baseline")
        _, context = evaluate_research(self.root, combined=True, ranking="page")
        self.assertEqual(baseline["passed"], 0)
        self.assertEqual(context["passed"], 1)
        self.assertEqual(context["anchor_hits_at_k"], 0)
        self.assertEqual(context["ranking"]["evidence_unit"], "parent_pdf_page")
        with self.assertRaisesRegex(ValueError, "inside evals"):
            evaluate_research(self.root, dataset_path="../outside.jsonl")

    def test_cli_and_evaluation_provenance(self):
        output = io.StringIO()
        with patch("sys.argv", ["mars-rag", "index", "example", "--root", str(self.root)]), contextlib.redirect_stdout(output):
            main()
        with patch("sys.argv", ["mars-rag", "search", "example", "second", "--root", str(self.root)]), contextlib.redirect_stdout(output):
            main()
        self.assertIn("PDF page 2", output.getvalue())
        source = json.loads((self.root / "sources/registry.json").read_text())["sources"][0]
        cases = [{"id": "second", "source_id": "example", "source_sha256": source["sha256"],
                  "question": "second", "expected_pages": [2], "expected_contains": ["Second page evidence"]}]
        path = self.root / "evals/example-retrieval.jsonl"
        path.parent.mkdir()
        path.write_text(json.dumps(cases[0]) + "\n")
        report_path, report = evaluate(self.root, "example", 1)
        self.assertEqual(report["passed"], 1)
        self.assertTrue(report_path.exists())
        cases[0]["source_sha256"] = "wrong"
        path.write_text(json.dumps(cases[0]) + "\n")
        with self.assertRaisesRegex(ValueError, "source version"):
            evaluate(self.root, "example", 1)

    def test_research_evaluation_leaves_gaps_unscored_and_checks_version(self):
        build_index(self.root, "example")
        source = json.loads((self.root / "sources/registry.json").read_text())["sources"][0]
        case = {"id": "partial", "question": "second", "expected_source_id": "example",
                "source_sha256": source["sha256"], "expected_pages": [2],
                "expected_contains": ["Second page evidence"], "evidence_status": "partial",
                "answer_boundary": "Relevant excerpt alone does not establish a complete answer."}
        gap = {"id": "gap", "question": "evidence", "evidence_status": "needs_review",
               "answer_boundary": "Shared words are not sufficient evidence."}
        path = self.root / "evals/research-retrieval.jsonl"
        path.parent.mkdir()
        path.write_text(json.dumps(case) + "\n" + json.dumps(gap) + "\n")
        _, report = evaluate_research(self.root, combined=True)
        self.assertEqual((report["passed"], report["total"], report["manual_gap_cases"]), (1, 1, 1))
        self.assertIsNone(report["results"][1]["passed"])
        self.assertTrue(report["results"][1]["chunk_ids"])
        self.assertIn("example", report["index_ids"])
        case["source_sha256"] = "wrong"
        path.write_text(json.dumps(case) + "\n")
        with self.assertRaisesRegex(ValueError, "source version"):
            evaluate_research(self.root, combined=True)


if __name__ == "__main__":
    unittest.main()
