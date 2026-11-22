"""Synthetic PDFs verify provenance, page boundaries, and preservation behavior."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import importlib.util

from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

from mars_rag.ingest import extract_source


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "data/raw").mkdir(parents=True)
        (self.root / "sources").mkdir()
        self.pdf = self.root / "data/raw/example.pdf"

    def prepare(self, blank=False, encrypted=False):
        writer = PdfWriter()
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                                 NameObject("/Subtype"): NameObject("/Type1"),
                                 NameObject("/BaseFont"): NameObject("/Helvetica")})
        for text in ["First page evidence", "Second page evidence"]:
            page = writer.add_blank_page(width=300, height=200)
            if not blank:
                page[NameObject("/Resources")] = DictionaryObject({
                    NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
                stream = DecodedStreamObject()
                stream.set_data(("BT /F1 12 Tf 20 100 Td (" + text + ") Tj ET").encode())
                page[NameObject("/Contents")] = writer._add_object(stream)
        writer.set_page_label(0, 1, style="/r")
        if encrypted:
            writer.encrypt("password")
        writer.write(self.pdf)
        self.source = {
            "source_id": "example", "filename": self.pdf.name,
            "local_path": "data/raw/example.pdf",
            "sha256": hashlib.sha256(self.pdf.read_bytes()).hexdigest(),
            "edition": "reviewed v2", "printed_page_labels": {"1": "A-1"},
        }
        self.save_register()

    def save_register(self):
        (self.root / "sources/registry.json").write_text(json.dumps({"sources": [self.source]}))

    def test_pages_preserve_evidence_and_distinct_labels(self):
        self.prepare()
        original = self.pdf.read_bytes()
        output, manifest = extract_source(self.root, "example")
        rows = [json.loads(line) for line in (output / "pages.jsonl").read_text().splitlines()]
        self.assertEqual([r["pdf_page_number"] for r in rows], [1, 2])
        self.assertIn("First page evidence", rows[0]["text"])
        self.assertNotIn("Second page evidence", rows[0]["text"])
        self.assertIn("Second page evidence", rows[1]["text"])
        self.assertEqual(rows[0]["printed_page_label"], "A-1")
        self.assertIsNone(rows[1]["printed_page_label"])
        self.assertEqual([r["pdf_page_label"] for r in rows], ["i", "ii"])
        self.assertTrue(all(r["source_sha256"] == self.source["sha256"] for r in rows))
        self.assertTrue(all(r["source_edition"] == "reviewed v2" for r in rows))
        self.assertEqual(manifest["pages_sha256"], hashlib.sha256((output / "pages.jsonl").read_bytes()).hexdigest())
        self.assertEqual(self.pdf.read_bytes(), original)

    def test_empty_pages_are_retained_and_flagged(self):
        self.prepare(blank=True)
        output, manifest = extract_source(self.root, "example")
        self.assertEqual(manifest["empty_text_pages"], [1, 2])
        self.assertEqual(len((output / "pages.jsonl").read_text().splitlines()), 2)

    def test_hash_mismatch_does_not_create_output(self):
        self.prepare()
        self.pdf.write_bytes(self.pdf.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            extract_source(self.root, "example")
        self.assertFalse((self.root / "data/processed").exists())

    def test_rerun_preserves_output_and_rejects_corruption(self):
        self.prepare()
        output, _ = extract_source(self.root, "example")
        stamp = (output / "pages.jsonl").stat().st_mtime_ns
        self.assertEqual(extract_source(self.root, "example")[0], output)
        self.assertEqual((output / "pages.jsonl").stat().st_mtime_ns, stamp)
        (output / "pages.jsonl").write_text("corrupted")
        with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
            extract_source(self.root, "example")
        self.assertEqual((output / "pages.jsonl").read_text(), "corrupted")

    def test_metadata_changes_create_separate_output(self):
        self.prepare()
        first, _ = extract_source(self.root, "example")
        self.source["edition"] = "corrected v3"
        self.save_register()
        second, _ = extract_source(self.root, "example")
        self.assertNotEqual(first, second)
        self.assertTrue((first / "pages.jsonl").exists())

    @unittest.skipUnless(importlib.util.find_spec("pdfplumber"), "optional spacing parser not installed")
    def test_spacing_parser_preserves_pages_and_prior_extraction(self):
        self.prepare()
        first, old = extract_source(self.root, "example")
        before = (first / "pages.jsonl").read_bytes()
        second, new = extract_source(self.root, "example", parser="pdfplumber")
        rows = [json.loads(x) for x in (second / "pages.jsonl").read_text().splitlines()]
        self.assertNotEqual(first, second)
        self.assertEqual(new["parser"], "pdfplumber")
        self.assertIn("pdfminer_version", new["settings"])
        self.assertEqual(new["source_sha256"], old["source_sha256"])
        self.assertEqual([p["pdf_page_number"] for p in rows], [1, 2])
        self.assertIn("First page evidence", rows[0]["text"])
        self.assertEqual(rows[0]["printed_page_label"], "A-1")
        self.assertEqual(rows[0]["pdf_page_label"], "i")
        self.assertEqual((first / "pages.jsonl").read_bytes(), before)
        self.assertEqual(extract_source(self.root, "example", parser="pdfplumber")[0], second)
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            extract_source(self.root, "example", parser="unknown")

    def test_unregistered_missing_and_outside_sources_fail(self):
        self.prepare()
        with self.assertRaisesRegex(ValueError, "found 0"):
            extract_source(self.root, "unknown")
        self.source["local_path"] = "outside.pdf"
        self.save_register()
        with self.assertRaisesRegex(ValueError, "inside data/raw"):
            extract_source(self.root, "example")
        self.source["local_path"] = "data/raw/missing.pdf"
        self.save_register()
        with self.assertRaises(FileNotFoundError):
            extract_source(self.root, "example")

    def test_encrypted_pdf_is_rejected(self):
        self.prepare(encrypted=True)
        with self.assertRaisesRegex(ValueError, "Encrypted"):
            extract_source(self.root, "example")
        self.assertFalse((self.root / "data/processed").exists())

    def test_malformed_pdf_does_not_write_output(self):
        self.prepare()
        self.pdf.write_bytes(b"not a PDF")
        self.source["sha256"] = hashlib.sha256(self.pdf.read_bytes()).hexdigest()
        self.save_register()
        with self.assertRaisesRegex(ValueError, "Cannot read PDF"):
            extract_source(self.root, "example")
        self.assertFalse((self.root / "data/processed").exists())


if __name__ == "__main__":
    unittest.main()
