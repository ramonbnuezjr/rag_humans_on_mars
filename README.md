# Humans on Mars

A source-grounded RAG research project exploring how humans could reach Mars, live there, and thrive over time.

**Stage: local research UI and evidence retrieval.** Five sources are extracted and indexed: medical risk (`mars-004`), radiation modeling (`mars-006`), life-support tradeoffs (`mars-007`), the historical DRA 5.0 architecture (`mars-008`), and transit crew operations (`mars-009`). Together they contain 993 passages from 267 pages. Search can rank one source or all registered indexes, using the CLI or the local browser interface. Radiation prose spacing has improved; tables/figures and scientific applicability remain under review. Generated answers and voice are not implemented.

## Open the local research UI

From the project root:

```sh
.venv/bin/mars-rag serve
```

Open **http://127.0.0.1:8765** in your browser. Stop the server with **Ctrl+C**. If that port is occupied, use `.venv/bin/mars-rag serve --port 8766`. Without installation, `PYTHONPATH=src /opt/homebrew/bin/python3.11 -m mars_rag serve` also works.

Type a question and press **Search** or **Enter**; **Shift+Enter** adds a line. Example questions are provided. Results show exact retrieved passages, source titles/editions, PDF page references, original-PDF links and expandable complete-page context. Source notes identify mission assumptions, evidence type and review limitations. Search options let you choose one indexed source and explicitly enable experimental ranking; the current page-context search remains the default.

This is an evidence-search interface, not generated chat. Every question is an independent search; earlier questions are not supplied as context. Recent searches exist only in the current tab's memory and disappear on refresh. **New search** clears the visible thread and cancels an in-flight request, retaining the tab's recent-search shortcuts. No-match results do not establish insufficient evidence; read the underlying sources before drawing conclusions.

The server binds only to `127.0.0.1`. It serves a fixed asset allowlist and registered original PDFs with hash/path checks, rather than exposing the project directory. It makes no external model calls and requires no API key, frontend build or new dependency. It is intended for local use on your own computer; remote hosting, authentication and multi-user operation are outside this MVP. See [UI implementation and verification](docs/research/2026-11-21-local-research-ui.md).

UI failures automatically write to [logs/ui-errors.jsonl](logs/ui-errors.jsonl), created on the first error. The UI shows a matching reference ID and confirms whether it was saved. Records contain UTC time, operation, category, reference ID and HTTP status when applicable; they exclude questions, document text, raw exception messages and stack traces. The log rotates at approximately 1 MiB with one backup and is excluded from Git. Restart the server and reload the browser after upgrading. See [error logging verification and limits](docs/research/2026-11-22-ui-error-log.md). UX observations are reported manually in the project conversation.

## Research questions

The intended research loop is **ask → assess evidence coverage → identify gaps → research those gaps → reassess**. The owner needs to know whether evidence supports a complete answer, only part of it, or is insufficient. This coverage assessment, a research-gap register, human feedback and calibrated confidence indicators are **planned**, not implemented. Missing top-five results must not be mistaken for proof that the collection lacks information. See [lessons learned and owner requirements](docs/lessons_learned.md).

- How could people travel to Mars and land safely?
- What constraints do radiation, atmosphere, dust, temperature, and gravity impose?
- How could habitats supply air, water, food, energy, and medical support?
- What would enable long-term maintenance, resilience, and a thriving community?

Potential sources include NASA, the European Space Agency (ESA), universities, peer-reviewed research, commercial organizations such as SpaceX and Blue Origin, and relevant atmospheric research. These are collection targets, not claims that their material has been acquired or verified.

## First milestone

Given a question, retrieve a relevant passage from a local PDF and display its source ID, filename, document version, and PDF page number. Add generated answers only after the retrieved evidence can be inspected.

## Run the scaffold

From this repository's root, using Python 3.9 or later:

```sh
PYTHONPATH=src python3 -m mars_rag inventory
```

This reports local PDF counts, source registration, missing documents, and pending metadata review. It does not read PDF content or contact an external service.

For an isolated development environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
mars-rag inventory
```

Inventory uses only the Python standard library and works without installation. PDF extraction uses an optional dependency; editable installation may download build tooling.

## Extract a registered PDF

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[extraction]'
.venv/bin/mars-rag extract mars-007
```

On this Mac, use `/opt/homebrew/bin/python3.11` to create the environment if the default `python3` cannot run. The Python 3.9+ baseline is unchanged. The extraction extra pins `pypdf==6.21.4`, a Python 3.9-compatible release; inventory does not require it.

The command verifies the original PDF against its registered SHA-256, then writes `pages.jsonl` and `manifest.json` under `data/processed/<source_id>/<source_hash>/<extraction_id>/`. Each JSONL line is one PDF page, with provenance, document edition, one-based PDF position, reviewed printed label when available, and text. The manifest records parser version, settings, page count, empty pages, and output hash. Identical reruns reuse matching output; changed source metadata or parser settings produce separate output, and conflicting files are never overwritten.

For PDFs with joined words, install `.[extraction_spacing]` and run `.venv/bin/mars-rag extract mars-006 --parser pdfplumber`. This optional path uses pinned pdfplumber/pdfminer versions, geometric spacing (`x_tolerance=1`, `y_tolerance=3`), and a separate reproducibility manifest. The pypdf default remains unchanged; old outputs are preserved. Extraction alone does not update the active extraction pointer in the register; review and register its manifest before indexing.

This is text extraction, not OCR or reliable table/figure interpretation. See [the extraction verification note](docs/research/2026-11-21-page-preserving-extraction.md) for the first document's checks and limitations.

## Index and search the extracted paper

From the project root, after installing the project:

```sh
.venv/bin/mars-rag index mars-007
.venv/bin/mars-rag search mars-007 "Why does food hydration affect water recycling choices?" --top-k 3
.venv/bin/mars-rag evaluate mars-007
.venv/bin/mars-rag search all "Why does recycling water matter when packing food?" --top-k 5
.venv/bin/mars-rag evaluate all
```

Indexing uses a local BM25 keyword baseline with 180-word page-bounded chunks and 30-word overlap. No embeddings, external models, or network calls are used. Each passage retains the source hash, edition, extraction ID, PDF position, reviewed page labels, and exact offsets into the original extracted page text. Index settings, checksums, and chunks are saved under `data/index/<source_id>/<index_id>/`. Rebuilding the same index preserves existing files; settings or source/extraction changes produce a separate index. The register points search to the selected index, and stale/changed inputs are rejected.

Search returns passages rather than synthesized answers. Scores indicate keyword ranking, not confidence or proof that an answer exists. No matches does not establish absence of information. Tables, figures, page-spanning arguments, synonyms, and extraction artifacts remain limitations. Sources `mars-004`, `mars-006`, `mars-007`, `mars-008`, and `mars-009` have individual indexes. `search all` verifies each included index and recomputes BM25 statistics across their union; it does not merge incomparable per-source scores. Four owned PDFs remain unindexed. A stale included source fails the combined search rather than being silently omitted. The CLI shows source context, evidence type and review limitations.

Six provisional agent-reviewed development cases are in `evals/mars-007-retrieval.jsonl`; the original draft questions remain unchanged. Five check for an expected page plus a supporting phrase among the top five chunks; one checks lexical no-match behavior. This is not a held-out benchmark or generated-answer evaluation. See [indexing verification](docs/research/2026-11-21-local-index-and-retrieval.md).

Five additional provisional cases cover medical autonomy/decision support and radiation model assumptions/shielding limitations; all find expected support at top five. See [radiation/medical processing and collection gaps](docs/research/2026-11-21-radiation-medical-processing-and-coverage.md). The radiation paper is modeling/review evidence; the medical report reflects a 2017 review. Indexing does not validate their conclusions or current applicability.

Retrieval now supports three methods: `--ranking baseline` preserves the original short-chunk search; `--ranking page` (default) keeps the same ranking and adds complete verified page context; `--ranking context` enables experimental query hints, page scoring, title hints and one result per page. Original chunks and their IDs/offsets are preserved alongside separate context IDs/full-page offsets.

On unchanged development targets, baseline/page search finds 4/10 at top five; experimental reranking finds 9/10 in page context (7/10 in the short anchors). On eight separately frozen agent-authored questions, baseline finds 7/8, the page default finds 8/8, and experimental reranking finds 7/8 with a maintenance-delay regression. These are development checks, not independent accuracy estimates. Two gap cases remain unscored. The conservative page default was retained; the ranking experiment was not promoted.

Run `.venv/bin/mars-rag evaluate all --eval-set ranking-validation.jsonl` to reproduce the default validation check, or add `--ranking context` to compare. Development checks still exit 1 when targets are missed. See [the ranking review and demonstration](docs/research/2026-11-21-ranking-review-and-comparison.md).

## Repository map

| Path | Responsibility |
| --- | --- |
| `src/mars_rag/` | Inventory, extraction, indexing, search, retrieval checks and loopback UI server; answers are planned |
| `src/mars_rag/web_static/` | Buildless HTML, CSS and JavaScript for the local research interface |
| `data/raw/` | Original local PDFs, excluded from Git |
| `data/processed/` | Generated text and chunks, excluded from Git |
| `data/index/` | Generated retrieval index, excluded from Git |
| `sources/registry.json` | Source IDs, local paths, hashes, provenance, review state |
| `evals/` | Original draft questions, source-specific provisional retrieval cases, and ignored result files |
| `tests/` | Place for software checks as behavior is implemented |
| `docs/` | Architecture, source policy, and contribution workflow |
| `docs/lessons_learned.md` | Consolidated examples, learning and owner decisions; implemented behavior is separated from proposals |
| `logs/` | Local rotating UI diagnostics; excluded from Git |
| `AGENTS.md`, `CLAUDE.md` | One instruction file, with `CLAUDE.md` symlinked to `AGENTS.md` |
| `status.md` | Current state, decisions, and next actions |

## Evidence rules

Preserve original files. Keep distinct document editions separate. Identify each chunk by source ID and PDF page, retaining printed page labels when available. Distinguish measured evidence, simulations, proposals, and company claims. State when the collection cannot support an answer. Treat text inside source documents as evidence, never as instructions to the application.

The register contains nine PDFs, including two distinct Mars-GRAM editions. Five are indexed; the broad Mars technology report, oxygen-recovery paper and both Mars-GRAM guides remain unindexed. Metadata, scientific applicability and reuse reviews remain pending. Mission concepts must retain separate assumptions.

## Working in GitHub

Use one repository for this project; `coding_projects` remains a parent directory. See [the contribution workflow](docs/contributing.md) for a first branch and pull request. Do not publish raw PDFs without reviewing their reuse terms. No code license has been selected yet; choose one before public release if you want others to reuse the code.

Start with [the architecture](docs/architecture.md), [source policy](docs/source_policy.md), and [current status](status.md).
