"""Small, bounded local diagnostic log. Never accepts free-text error details."""

from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import uuid


OPERATIONS = {"search", "collection", "pdf", "request", "browser", "feedback"}
CATEGORIES = {"http_error", "network", "unreadable_response", "javascript", "unexpected"}


class ErrorLog:
    def __init__(self, root, max_bytes=1024 * 1024):
        self.path = Path(root) / "logs/ui-errors.jsonl"
        self.max_bytes = max_bytes
        self.lock = threading.Lock()

    def record(self, operation, category, http_status=None):
        if operation not in OPERATIONS or category not in CATEGORIES:
            raise ValueError("Unknown diagnostic category or operation.")
        event = {"timestamp": datetime.now(timezone.utc).isoformat(),
                 "error_id": uuid.uuid4().hex, "operation": operation, "category": category}
        if http_status is not None:
            event["http_status"] = http_status
        try:
            with self.lock:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                if self.path.exists() and self.path.stat().st_size >= self.max_bytes:
                    # One backup: at most approximately 2 MiB in total.
                    self.path.replace(self.path.with_suffix(".jsonl.1"))
                with self.path.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(event) + "\n")
            return event["error_id"], True
        except OSError:
            return event["error_id"], False
