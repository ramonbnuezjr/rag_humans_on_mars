# Local UI error log

Date: 2026-11-22. Implementation and verification record; no mission research added.

## Implemented

- [Server](../../src/mars_rag/web.py) records unsuccessful JSON responses, including search, collection and PDF failures. Unexpected application exceptions return a generic error. Existing request access logs remain disabled.
- [Browser](../../src/mars_rag/web_static/app.js) reports caught search/collection failures without server receipts, unexpected JavaScript errors and unhandled promise rejections. Server receipts are reused rather than logged again. Deliberate search cancellation and normal no-match results are not errors.
- [Error log writer](../../src/mars_rag/error_log.py) appends one JSON object per line to [logs/ui-errors.jsonl](../../logs/ui-errors.jsonl), creating it on the first error. Each record has UTC timestamp, random reference ID, operation, category and optional HTTP status. No questions, PDF text, URLs, headers, raw exception messages or stack traces are accepted. Browser diagnostic submissions allow only the two fixed operation/category fields.
- Writes are serialized within the server process. At approximately 1 MiB the file rotates to `ui-errors.jsonl.1`, replacing the previous backup. These files are excluded from Git and are not served through the web UI. Run one application server per project in ordinary use; cross-process locking is outside this small MVP.
- UI errors confirm saving and show the matching reference ID. If the server or disk cannot accept the event, the UI says the log could not be saved. Browser diagnostic submission has a two-second timeout. There is no browser storage, deferred retry queue or external telemetry.

## Verification

31 Python tests pass, including HTTP integration, safe fields, unexpected failures, unwritable storage, concurrent writes and rotation. JavaScript syntax check passes.

An isolated browser preview on port 8766 deliberately sent an invalid ranking. The UI displayed reference `6e580fc0a6f043d384e0069bef192523`, exactly matching the persisted HTTP 400 record. Its private test question was absent from the file. A simulated failed search request produced network reference `ecfcf7b497ff4639ba6133a2034368ba`. A dispatched JavaScript error produced reference `7515721b340a484caa115b9eb9796f25`; its raw message was excluded. Blocking the diagnostic endpoint displayed “could not be saved.” After removing the fault injection, a normal water-recycling search returned five passages. Test-generated diagnostic records are retained in the local log as examples; they are not user-reported defects.

## Activation and limits

Restart the existing server with `.venv/bin/mars-rag serve` and reload the page to load both server and browser changes. The separate verification server is stopped after testing.

This is best-effort local diagnostics, not comprehensive monitoring. Server downtime, browser crashes, failures before the JavaScript loads and some asset-loading failures may prevent capture. Error categories help identify a failure but deliberately omit detailed exception context; reproduction may still be necessary. Rotation discards older records. UX concerns such as confusing wording or layout remain manually reported in the project conversation. No issue-reporting UI, AI service, document changes or research collection changes were added.
