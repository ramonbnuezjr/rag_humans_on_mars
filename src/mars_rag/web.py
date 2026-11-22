"""Loopback-only research UI for existing local retrieval; no model services."""

import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from urllib.parse import quote, urlsplit

from .index import load_index
from .error_log import ErrorLog, OPERATIONS, CATEGORIES
from .retrieve import indexed_source_ids, search


ASSETS = Path(__file__).parent / "web_static"


def source_records(root):
    registry = json.loads((Path(root) / "sources/registry.json").read_text(encoding="utf-8"))
    return {s["source_id"]: s for s in registry["sources"]}


def collection(root):
    records = source_records(root)
    sources = []
    pages = passages = 0
    for sid in indexed_source_ids(root):
        manifest, _ = load_index(root, sid)
        pages += manifest["page_count"]
        passages += manifest["chunk_count"]
        sources.append({"source_id": sid, "title": records[sid].get("title") or sid})
    return {"registered": len(records), "indexed": len(sources), "pages": pages,
            "passages": passages, "sources": sources}


def search_response(root, payload):
    if not isinstance(payload, dict):
        raise ValueError("Search request must be a JSON object.")
    question = payload.get("question")
    if not isinstance(question, str) or not 1 <= len(question.strip()) <= 2000:
        raise ValueError("Enter a question between 1 and 2,000 characters.")
    sid = payload.get("source_id", "all")
    if not isinstance(sid, str) or sid not in ["all"] + indexed_source_ids(root):
        raise ValueError("Choose an indexed source or the whole collection.")
    ranking = payload.get("ranking", "page")
    if ranking not in ("page", "context", "baseline"):
        raise ValueError("Unknown search method.")
    hits = search(root, sid, question.strip(), 5, ranking=ranking)
    records = source_records(root)
    results = []
    for hit in hits:
        source = records[hit["source_id"]]
        results.append({
            "source_id": hit["source_id"], "title": hit.get("source_title") or hit["source_filename"],
            "filename": hit["source_filename"], "edition": hit.get("source_edition"),
            "pdf_page": hit["pdf_page_number"], "printed_page": hit.get("printed_page_label"),
            "passage": hit["text"], "page_context": hit.get("context_text"),
            "pdf_url": "/api/sources/{}/pdf#page={}".format(hit["source_id"], hit["pdf_page_number"]),
            "mission_context": source.get("mission_context"), "evidence_type": source.get("evidence_type"),
            "metadata_status": source.get("metadata_status"),
            "limitations": source.get("extraction", {}).get("quality_limitations", []),
            "provenance": {k: hit.get(k) for k in ("source_sha256", "extraction_id", "index_id",
                            "chunk_id", "context_id", "char_start", "char_end",
                            "context_char_start", "context_char_end")},
        })
    return {"question": question.strip(), "ranking": ranking, "results": results,
            "notice": "Retrieved passages, not a generated answer. Matches may provide only partial evidence."
                      if results else "No keyword matches found. This does not establish that the collection lacks the information."}


def make_server(root, port=8765):
    root = Path(root).resolve()
    error_log = ErrorLog(root)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass  # Do not log question text, headers or local document paths.

        def allowed(self):
            allowed_hosts = {"127.0.0.1:{}".format(self.server.server_port),
                             "localhost:{}".format(self.server.server_port)}
            if self.headers.get("Host") not in allowed_hosts:
                self.send_json(403, {"error": "Use the local application address."})
                return False
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://" + host for host in allowed_hosts}:
                self.send_json(403, {"error": "Cross-origin requests are not allowed."})
                return False
            return True

        def send_body(self, status, data, content_type, disposition=None):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; "
                             "connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; "
                             "frame-ancestors 'none'; form-action 'self'")
            if disposition:
                self.send_header("Content-Disposition", disposition)
            self.end_headers()
            self.wfile.write(data)

        def send_json(self, status, value):
            if status >= 400 and urlsplit(self.path).path != "/api/ui-errors":
                path = urlsplit(self.path).path
                operation = "search" if path == "/api/search" else "collection" if path == "/api/collection" else "pdf" if path.endswith("/pdf") else "request"
                error_id, saved = error_log.record(operation, "http_error", status)
                value = dict(value, error_id=error_id, logged=saved)
            self.send_body(status, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

        def do_GET(self):
            if not self.allowed():
                return
            path = urlsplit(self.path).path
            assets = {"/": ("index.html", "text/html; charset=utf-8"),
                      "/static/app.css": ("app.css", "text/css; charset=utf-8"),
                      "/static/app.js": ("app.js", "text/javascript; charset=utf-8")}
            try:
                if path in assets:
                    name, content_type = assets[path]
                    self.send_body(200, (ASSETS / name).read_bytes(), content_type)
                elif path == "/api/collection":
                    self.send_json(200, collection(root))
                elif re.fullmatch(r"/api/sources/[A-Za-z0-9_-]+/pdf", path):
                    sid = path.split("/")[3]
                    source = source_records(root).get(sid)
                    if not source:
                        self.send_json(404, {"error": "Source not found."})
                        return
                    file = (root / source["local_path"]).resolve()
                    if (root / "data/raw").resolve() not in file.parents or file.suffix.lower() != ".pdf":
                        self.send_json(403, {"error": "Source is outside the local PDF collection."})
                        return
                    data = file.read_bytes()
                    if hashlib.sha256(data).hexdigest() != source["sha256"]:
                        self.send_json(409, {"error": "Original PDF changed; review the source register before opening."})
                        return
                    self.send_body(200, data, "application/pdf",
                                   "inline; filename*=UTF-8''" + quote(file.name, safe=""))
                else:
                    self.send_json(404, {"error": "Not found."})
            except (OSError, ValueError, KeyError):
                self.send_json(503, {"error": "The local collection is unavailable. Check the project setup and source indexes."})
            except Exception:
                self.send_json(500, {"error": "An unexpected local application error occurred."})

        def do_POST(self):
            if not self.allowed():
                return
            path = urlsplit(self.path).path
            if path not in {"/api/search", "/api/ui-errors"}:
                self.send_json(404, {"error": "Not found."})
                return
            if self.headers.get_content_type() != "application/json":
                self.send_json(415, {"error": "Search requires JSON."})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 16000:
                    self.send_json(413, {"error": "Search request is too large or empty."})
                    return
                payload = json.loads(self.rfile.read(size).decode("utf-8"))
                if path == "/api/ui-errors":
                    if (not isinstance(payload, dict) or set(payload) != {"operation", "category"}
                            or not isinstance(payload["operation"], str) or payload["operation"] not in OPERATIONS
                            or not isinstance(payload["category"], str) or payload["category"] not in CATEGORIES):
                        raise ValueError("Use only the supported diagnostic fields.")
                    error_id, saved = error_log.record(payload["operation"], payload["category"])
                    self.send_json(200, {"error_id": error_id, "logged": saved})
                    return
                response = search_response(root, payload)
                self.send_json(200, response)
            except (ValueError, UnicodeError) as error:
                self.send_json(400, {"error": str(error)})
            except (OSError, KeyError):
                self.send_json(503, {"error": "Search could not read a verified index. Check the project setup."})
            except Exception:
                self.send_json(500, {"error": "An unexpected local application error occurred."})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def serve(root, port=8765):
    server = make_server(root, port)
    print("Humans on Mars: http://127.0.0.1:{}".format(server.server_port), flush=True)
    print("Local evidence search. No generated answers. Stop with Ctrl+C.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
