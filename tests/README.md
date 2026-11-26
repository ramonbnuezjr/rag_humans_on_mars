# Software tests

`test_ingest.py` creates small synthetic two-page PDFs to check page boundaries and provenance, separation of printed and embedded labels, empty pages, hash mismatches, missing/unknown sources, encrypted documents, metadata changes, and preservation of existing output.

Install the extraction extra, then run from the project root:

```sh
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

`test_index.py` adds synthetic end-to-end checks for exact chunk offsets/overlap, provenance and labels, ranking and no-match behavior, unchanged originals, altered inputs, stale metadata, immutable reruns, corrupted index handling, CLI output, and evaluation source-version matching.

The tests use synthetic fixtures, not the local research PDFs, so they can run without distributing source documents. Thirty-four software tests currently pass with spacing support installed. Provisional retrieval checks against the local paper live in `evals/mars-007-retrieval.jsonl` and run separately with `mars-rag evaluate mars-007`; these require the private PDF, extraction, and index. Generated-answer checks remain future work.

`test_web.py` starts an ephemeral loopback server using synthetic indexed PDFs. It checks fixed asset routes, collection metadata, real search/provenance/context responses, no-match handling, malformed requests, origin/host boundaries, original-PDF serving, hash changes, path boundaries and broken-index errors. These tests require permission to bind a local socket. Visual layout and browser interactions were checked separately; they are not assertions in this Python suite.

Use small synthetic or redistributable fixtures. Research answer quality belongs in `evals/`; software tests and research evaluations serve different purposes.

Error-log tests verify matching response/log references, strict diagnostic field validation, exclusion of private query/exception strings, unexpected server failures, unwritable storage, rotation and concurrent writes. Browser checks separately verify error presentation, diagnostic submission, save-failure feedback and successful search recovery. See [verification notes](../docs/research/2026-11-22-ui-error-log.md).

The suite now has 34 passing tests, including feedback persistence across store instances, all rating choices, idempotent retries, revision history and latest-only counts, snapshot provenance, tampering rejection, origin boundaries, no-match reviews and storage-failure isolation. Synthetic browser checks additionally covered save, edit, network failure, retained input, retry and reload persistence; QA reviews were kept outside the real project store.
