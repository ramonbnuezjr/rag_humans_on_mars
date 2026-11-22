"""Local HTTP integration checks with synthetic sources, not private PDFs."""

import http.client
import json
import threading
import unittest
from unittest.mock import patch

import test_index
from mars_rag.index import build_index
from mars_rag.web import make_server


class WebTests(unittest.TestCase):
    def setUp(self):
        fixture = test_index.IndexTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        build_index(self.root, "example")
        self.server = make_server(self.root, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def request(self, path, payload=None, headers=None, body=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        self.addCleanup(connection.close)
        request_headers = dict(headers or {})
        method = "POST" if payload is not None or body is not None else "GET"
        if payload is not None:
            body = json.dumps(payload)
            request_headers.setdefault("Content-Type", "application/json")
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read()

    def test_assets_collection_and_narrow_routes(self):
        status, headers, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertIn(b"Your research question", body)
        self.assertIn("script-src 'self'", headers["Content-Security-Policy"])
        self.assertEqual(headers["Cache-Control"], "no-store")
        for path in ("/static/app.css", "/static/app.js"):
            self.assertEqual(self.request(path)[0], 200)
        for path in ("/sources/registry.json", "/.env", "/static/../web.py", "/data/raw/example.pdf"):
            self.assertEqual(self.request(path)[0], 404)
        status, _, body = self.request("/api/collection")
        data = json.loads(body)
        self.assertEqual((status, data["indexed"], data["pages"], data["passages"]), (200, 1, 2, 2))

    def test_real_retrieval_context_provenance_and_no_match(self):
        status, _, body = self.request("/api/search", {"question": "second"})
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(data["ranking"], "page")
        hit = data["results"][0]
        self.assertEqual(hit["pdf_page"], 2)
        self.assertEqual(hit["pdf_url"], "/api/sources/example/pdf#page=2")
        self.assertIn("Second page evidence", hit["page_context"])
        self.assertTrue(hit["provenance"]["source_sha256"])
        self.assertTrue(hit["provenance"]["chunk_id"])
        self.assertIn("not a generated answer", data["notice"])
        for ranking in ("context", "baseline"):
            status, _, body = self.request("/api/search", {"question": "second", "source_id": "example", "ranking": ranking})
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)["results"][0]["pdf_page"], 2)
        status, _, body = self.request("/api/search", {"question": "platypus"})
        self.assertEqual(json.loads(body)["results"], [])
        self.assertIn("does not establish", json.loads(body)["notice"])

    def test_input_validation_and_origin_boundaries(self):
        for payload in ({"question": " "}, {"question": "x" * 2001}, {"question": "second", "source_id": "unknown"},
                        {"question": "second", "ranking": "unknown"}, {"question": 42}, [], {"question": "the and"}):
            self.assertEqual(self.request("/api/search", payload)[0], 400)
        self.assertEqual(self.request("/api/search", body="{", headers={"Content-Type": "application/json"})[0], 400)
        self.assertEqual(self.request("/api/search", body="{}", headers={"Content-Type": "text/plain"})[0], 415)
        self.assertEqual(self.request("/api/search", {"question": "second"}, headers={"Origin": "https://example.com"})[0], 403)
        self.assertEqual(self.request("/", headers={"Host": "example.com"})[0], 403)

    def test_pdf_serving_hash_and_path_boundaries(self):
        status, headers, body = self.request("/api/sources/example/pdf")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "application/pdf")
        original = self.root / "data/raw/example.pdf"
        self.assertEqual(body, original.read_bytes())
        original.write_bytes(body + b"changed")
        self.assertEqual(self.request("/api/sources/example/pdf")[0], 409)
        self.assertEqual(self.request("/api/sources/unknown/pdf")[0], 404)
        path = self.root / "sources/registry.json"
        registry = json.loads(path.read_text())
        registry["sources"][0]["local_path"] = "sources/secret.pdf"
        path.write_text(json.dumps(registry))
        self.assertEqual(self.request("/api/sources/example/pdf")[0], 403)

    def test_broken_index_returns_visible_error_without_partial_results(self):
        path = self.root / "sources/registry.json"
        source = json.loads(path.read_text())["sources"][0]
        manifest = self.root / source["index"]["manifest_path"]
        (manifest.parent / "index.json").write_text("changed")
        self.assertEqual(self.request("/api/collection")[0], 503)
        status, _, body = self.request("/api/search", {"question": "second"})
        self.assertEqual(status, 400)
        self.assertIn("checksum", json.loads(body)["error"])

    def test_error_reference_matches_private_local_log(self):
        secret = "PRIVATE QUESTION CONTENT"
        status, _, body = self.request("/api/search", {"question": secret, "ranking": "invalid"})
        receipt = json.loads(body)
        self.assertEqual(status, 400)
        self.assertTrue(receipt["logged"])
        log = self.root / "logs/ui-errors.jsonl"
        event = json.loads(log.read_text())
        self.assertEqual(event["error_id"], receipt["error_id"])
        self.assertEqual(event["operation"], "search")
        self.assertEqual(event["http_status"], 400)
        self.assertNotIn(secret, log.read_text())
        self.assertEqual(set(event), {"timestamp", "error_id", "operation", "category", "http_status"})
        self.assertEqual(self.request("/logs/ui-errors.jsonl")[0], 404)

    def test_browser_diagnostics_accept_only_fixed_fields(self):
        status, _, body = self.request("/api/ui-errors", {"operation": "browser", "category": "javascript"})
        self.assertEqual(status, 200)
        event = json.loads((self.root / "logs/ui-errors.jsonl").read_text())
        self.assertEqual(event["error_id"], json.loads(body)["error_id"])
        for payload in ({"operation": "browser", "category": "javascript", "message": "PRIVATE"},
                        {"operation": "PRIVATE", "category": "network"},
                        {"operation": [], "category": "network"}):
            self.assertEqual(self.request("/api/ui-errors", payload)[0], 400)
        self.assertNotIn("PRIVATE", (self.root / "logs/ui-errors.jsonl").read_text())

    def test_unexpected_failure_and_unwritable_log(self):
        with patch("mars_rag.web.search_response", side_effect=RuntimeError("PRIVATE")):
            status, _, body = self.request("/api/search", {"question": "second"})
        self.assertEqual(status, 500)
        self.assertNotIn(b"PRIVATE", body)
        self.assertNotIn("PRIVATE", (self.root / "logs/ui-errors.jsonl").read_text())
        with patch("mars_rag.error_log.Path.open", side_effect=PermissionError):
            status, _, body = self.request("/api/ui-errors", {"operation": "search", "category": "network"})
        self.assertEqual(status, 200)
        self.assertFalse(json.loads(body)["logged"])

    def test_log_rotation_and_concurrent_records(self):
        from mars_rag.error_log import ErrorLog
        log = ErrorLog(self.root, max_bytes=1)
        first, _ = log.record("search", "network")
        second, _ = log.record("browser", "javascript")
        self.assertEqual(json.loads(log.path.with_suffix(".jsonl.1").read_text())["error_id"], first)
        self.assertEqual(json.loads(log.path.read_text())["error_id"], second)
        log.max_bytes = 1024 * 1024
        threads = [threading.Thread(target=log.record, args=("search", "network")) for _ in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        events = [json.loads(line) for line in log.path.read_text().splitlines()]
        self.assertEqual(len(events), 21)
        self.assertEqual(len({event["error_id"] for event in events}), 21)


if __name__ == "__main__":
    unittest.main()
