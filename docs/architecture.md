# Architecture and build sequence

## Boundaries

A minimal local browser UI is implemented in `src/mars_rag/web.py` and `web_static/`. It wraps the existing retrieval API; it does not implement generated answers or evidence sufficiency. `serve` binds only to loopback, serves an explicit asset allowlist and hash-checked registered PDFs, and accepts bounded JSON searches. Browser text is inserted with `textContent`, never treated as HTML. No framework, external assets or provider credentials are required. Search history is tab memory only; each request is independent. See [UI verification](research/2026-11-21-local-research-ui.md).

Local diagnostic logging is implemented: unsuccessful JSON responses and browser-reported errors receive reference IDs, with fixed-field records in ignored `logs/ui-errors.jsonl`. Rotation keeps one backup. No query text, document text or raw exception details are logged. Server downtime can prevent browser reports from being saved; the UI reports save failure. See [diagnostic verification and limits](research/2026-11-22-ui-error-log.md).

Keep collection, extraction, indexing, retrieval, and answer generation separate. This makes it possible to identify whether a bad answer came from an unreadable PDF, missing text, poor retrieval, or unsupported generation.

| Stage | Input | Output | Current state |
| --- | --- | --- | --- |
| Collection inventory | Local files and source register | Counts and missing/unregistered paths | Implemented |
| Extraction | One registered PDF | Page text with source ID and page references | Implemented for five sources; sampled prose reviewed; optional geometric spacing improves radiation text |
| Indexing | Extracted page text | Page-bounded chunks and local BM25 index | Five separate indexes; combined BM25 over a verified union |
| Retrieval | Question and index | Ranked passages with source metadata | Local keyword baseline implemented |
| Answer generation | Question and retrieved passages | Evidence-grounded answer with citations | Planned |
| Evaluation | Provisional questions and expected evidence | Top-k evidence checks | Eleven earlier checks plus twelve realistic draft questions; gaps unscored; answer evaluation not implemented |
| Evidence coverage and research gaps | Question, mission scope, evidence and review | Supported/partial/insufficient assessment and specific evidence needs | Owner requirement recorded; not implemented |
| Human feedback and confidence | Reviewed relevance and coverage judgments | Versioned feedback and eventually calibrated estimates | Proposed; no buttons, persistent feedback or numerical confidence |

## Intended evidence-coverage loop

The owner prioritizes knowing whether the available evidence can answer a question completely. The planned workflow is ask, assess coverage, identify gaps, research those gaps and reassess. A relevance score alone does not satisfy this requirement. Define the question's parts and applicable mission concept; cite support for each part, expose contradictions and record what remains unsupported. “Supported” must be relative to that scope and reviewed evidence, not a guarantee of exhaustive scientific knowledge.

A failed retrieval must be investigated before declaring a collection gap. Relevant material may already exist in extracted text but rank below the displayed results. Proposed gap records should distinguish retrieval misses, candidate collection gaps and owner-reviewed gaps, retain evidence/version references and specify what additional evidence would help. Passage-level relevance and question-level coverage feedback serve different purposes. No automatic downloads or ranking changes follow from feedback today. Numerical confidence requires a defined target, reviewed cases and separate calibration/testing; BM25 scores are not coverage probabilities.

## Evidence record

Each extracted page should retain `source_id`, `source_sha256`, `pdf_page_number` (one-based), optional `printed_page_label`, and `text`. Chunks should additionally have a stable chunk identifier and their page span. Never substitute PDF viewer page positions for printed page numbers without labeling the distinction.

The extraction command writes one JSON object per page to `pages.jsonl`, with source filename, local path, title, edition, and canonical URL as well. `pdf_page_label` is populated only from an embedded PDF label dictionary. `printed_page_label` comes only from manually reviewed `printed_page_labels` metadata in the source register; otherwise it is null. These are distinct from the mandatory PDF page position. Empty pages remain in the sequence with a warning.

`manifest.json` records the parser and extractor versions, extraction settings, source hash, page metadata hash, page count, empty-page positions, and SHA-256 of the JSONL output. Output paths include full source and extraction hashes. The extraction ID incorporates parser/settings and page metadata, including edition and reviewed labels. Identical reruns verify and reuse output; conflicts fail without overwriting. Registry changes require extraction to be rerun to propagate corrected metadata. Extraction does not mark a source as scientifically reviewed or indexed.

Track document edition separately from extraction and index versions. A new edition is a new source; re-running extraction is a new processing run. Record parser version, chunk size and overlap, embedding model if used, and retrieval settings so changes can be compared.

## First vertical slice

1. Verify one PDF and its source register entry.
2. Extract a few pages; manually inspect prose, units, equations, and tables.
3. Write several questions with known supporting passages.
4. Build a simple retrieval baseline and show the returned evidence.
5. Compare retrieval results against the known passages.
6. Choose a generation provider and document any external data transfer.
7. Add answers that cite evidence and state when evidence is insufficient.

The first text parser is the optional `pypdf==6.21.4` dependency, retaining Python 3.9 support. Plain text mode is used without normalization or OCR. Source layout may not survive extraction; tables, formulas, images, and plots require separate checks before evidence is used. The first retrieval baseline uses Python's standard library for local BM25 ranking over a JSON inverted index. No generation model, hosted database, or orchestration framework is selected. Local document storage alone does not make an application sovereign: embeddings, generation, telemetry, and remote APIs also determine where data goes. Extraction, indexing, and search themselves call no network or model service.

## Local index and retrieval baseline

Chunks are exact substrings of individual page records: 180 whitespace-delimited words with 30-word overlap. They never cross a page. Each retains source ID/hash, filename/title/edition/URL, extraction ID, PDF start/end positions, embedded and reviewed printed labels, extraction warnings, and character offsets. Stable chunk IDs derive from source hash, extraction ID, page position, offsets, and text checksum.

The index stores term postings, term frequencies, and passage lengths. Tokenization uses lowercase ASCII alphanumeric sequences and a fixed stop-word list; there is no stemming, synonym expansion, semantic embedding, or reranker. BM25 uses `k1=1.2`, `b=0.75`; the score is not a probability. The index manifest records settings, source/extraction identities, page and index checksums, and limitations. A deterministic index ID names the immutable output directory. The source register selects the active index per source.

Build and search verify the original file, current extraction pointer, page sequence, output checksum, and source/page-label metadata. Search also verifies the index checksum and rejects stale extraction identities. Source review status remains independent of indexing status. Changing metadata requires re-extraction and rebuilding, rather than relabeling old chunks in place.

Search accepts one explicitly named source or `all` registered indexes and returns complete passages with provenance. Combined retrieval recomputes term frequencies, document frequencies and average passage length across the union, retaining individual index identities. All included indexes must have matching retrieval/chunk settings. Invalid included indexes fail the search rather than silently narrowing coverage. Source context/caveats are displayed by the CLI; document concepts are not reconciled automatically. It does not synthesize answers or infer sufficient/insufficient evidence from scores. An out-of-vocabulary query returns no matches; a question containing generic shared words can still return irrelevant passages. Page-bound chunks may omit adjacent-page context or qualifications; numerical and table-based claims remain unvalidated.

## Later concerns

Inspect citations for entailment, measure latency and cost, expose index freshness, handle contradictory sources, and test malicious instructions embedded in source text. Expand the collection after the first slice works so ingestion problems remain diagnosable.

## Optional spacing extraction and research checks

The pypdf path is unchanged. The optional `extraction_spacing` extra pins pdfplumber 0.11.8 and pdfminer.six 20251107. It extracts each page using geometric spacing with x tolerance 1 point and y tolerance 3 points, without OCR or guessed word reconstruction. Parser/dependency versions, settings, labels and source hash participate in extraction identity. Pypdf still supplies page-label metadata and initial PDF validation. The radiation source now selects this separate extraction; its old extraction/index pointers are retained in register history. This is sampled prose improvement, not structured table extraction.

The realistic question evaluation records active source hashes/index IDs, dataset checksum, query text, expected-page/phrase hits and returned source/page/chunk IDs. Partial-evidence targets test passage location only; unanswered/gap labels remain manual and unscored. Initial three-source cases and results are preserved separately from the expanded five-source cases. Narrow labels can miss other relevant evidence. No answer generation or automated evidence-sufficiency classifier is implemented.

## Ranking experiment and parent-page context

Search defaults to `page`: original chunk BM25 order/scores plus verified complete-page context. Anchor IDs/text/offsets are unchanged; page text has separate context IDs and full-page offsets. `baseline` reproduces short-chunk search. Experimental `context` combines chunk score with 0.7 times parent-page BM25, 0.5-weight glossary expansions, limited 0.4 subject-word title boosts, and one result per page. Settings and explicit terminology live in `src/mars_rag/ranking.py`; no source/page/case-specific rules or model services are used. Immutable indexes are not rebuilt.

Evaluation records method/configuration hash, separate anchor and context hits, dataset identity and active index/source snapshot. Evidence location in a returned full page is different from location in its short anchor. Validation exposed a ranking regression, so the experiment remains opt-in. See [the comparison](research/2026-11-21-ranking-review-and-comparison.md). Full-page context is not adjacent-page expansion, structured table interpretation or evidence-sufficiency classification.
