"""Owner coverage judgments tied to signed retrieval snapshots; no model calls."""

from datetime import datetime, timezone
from contextlib import contextmanager
import hashlib
import hmac
import json
from pathlib import Path
import secrets
import sqlite3
import uuid


RATINGS = ("fully", "partially", "not_at_all", "unsure")


class FeedbackStore:
    def __init__(self, root):
        self.path = Path(root) / "feedback/reviews.sqlite3"

    @contextmanager
    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(str(self.path), timeout=5)
        try:
            db.execute("CREATE TABLE IF NOT EXISTS settings (name TEXT PRIMARY KEY, value TEXT NOT NULL)")
            db.execute("INSERT OR IGNORE INTO settings VALUES ('signing_key', ?)", (secrets.token_hex(32),))
            db.execute("""CREATE TABLE IF NOT EXISTS reviews (
                event_id TEXT PRIMARY KEY, search_id TEXT NOT NULL, rating TEXT NOT NULL,
                note TEXT NOT NULL, recorded_at TEXT NOT NULL, snapshot TEXT NOT NULL)""")
            db.commit()
            with db:
                yield db
        finally:
            db.close()

    def signature(self, snapshot):
        with self.connect() as db:
            key = db.execute("SELECT value FROM settings WHERE name='signing_key'").fetchone()[0]
        body = json.dumps(snapshot, sort_keys=True, ensure_ascii=True).encode("utf-8")
        return hmac.new(key.encode("ascii"), body, hashlib.sha256).hexdigest()

    def receipt(self, response, source_id):
        registry = json.loads((self.path.parent.parent / "sources/registry.json").read_text())
        snapshot = {"search_id": uuid.uuid4().hex, "searched_at": datetime.now(timezone.utc).isoformat(),
                    "question": response["question"], "source_filter": source_id,
                    "ranking": response["ranking"], "top_k": 5,
                    "corpus": [{"source_id": s["source_id"], "source_sha256": s["sha256"],
                                "index": s["index"]} for s in registry["sources"]
                               if s.get("index") and source_id in ("all", s["source_id"])],
                    "retrieval_code_sha256": hashlib.sha256(b"".join(
                        Path(__file__).with_name(name).read_bytes()
                        for name in ("index.py", "retrieve.py", "ranking.py"))).hexdigest(),
                    "evidence": [{"source_id": r["source_id"], "pdf_page": r["pdf_page"],
                                  "edition": r["edition"], **r["provenance"]}
                                 for r in response["results"]]}
        return {"snapshot": snapshot, "signature": self.signature(snapshot)}

    def save(self, payload):
        if not isinstance(payload, dict) or set(payload) != {"receipt", "rating", "note"}:
            raise ValueError("Provide a search receipt, rating and note.")
        rating, note, receipt = payload["rating"], payload["note"], payload["receipt"]
        if not isinstance(rating, str) or rating not in RATINGS:
            raise ValueError("Choose Fully, Partially, Not at all or Unsure.")
        if not isinstance(note, str) or len(note) > 2000:
            raise ValueError("Keep the feedback note within 2,000 characters.")
        if (not isinstance(receipt, dict) or set(receipt) != {"snapshot", "signature"}
                or not isinstance(receipt["snapshot"], dict) or not isinstance(receipt["signature"], str)
                or len(receipt["signature"]) != 64 or any(c not in "0123456789abcdef" for c in receipt["signature"])
                or not hmac.compare_digest(receipt["signature"], self.signature(receipt["snapshot"]))):
            raise ValueError("This search reference is invalid. Search again before reviewing.")
        snapshot = receipt["snapshot"]
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT event_id, rating, note FROM reviews WHERE search_id=? ORDER BY rowid DESC LIMIT 1",
                                  (snapshot["search_id"],)).fetchone()
            if previous and previous[1:] == (rating, note.strip()):
                return {"saved": True, "feedback_id": previous[0]}
            event_id = uuid.uuid4().hex
            db.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?)",
                       (event_id, snapshot["search_id"], rating, note.strip(),
                        datetime.now(timezone.utc).isoformat(), json.dumps(snapshot)))
        return {"saved": True, "feedback_id": event_id}

    def summary(self):
        # Count each search once using its latest judgment; retain all revisions on disk.
        with self.connect() as db:
            rows = db.execute("""SELECT rating, note, recorded_at, snapshot FROM reviews
                WHERE rowid IN (SELECT MAX(rowid) FROM reviews GROUP BY search_id)
                ORDER BY rowid DESC""").fetchall()
        counts = {rating: 0 for rating in RATINGS}
        for rating, *_ in rows:
            counts[rating] += 1
        return {"total": len(rows), "counts": counts,
                "recent": [{"rating": r, "note": n, "recorded_at": t, "question": json.loads(s)["question"]}
                           for r, n, t, s in rows[:5]]}
