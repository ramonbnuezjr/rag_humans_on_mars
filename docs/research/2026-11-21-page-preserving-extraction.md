# Page preserving extraction of the life support tradeoff paper

Date: 2026-11-21 (America/New_York)

Source: `mars-007`, [the local life-support tradeoff paper](<../../data/raw/ECLSS Does Not Exist in a Vacuum v9 (unlinked citations).pdf>). The title, context, source-record links, and preliminary research questions are in [the inspection report](2026-11-21-initial-pdf-inspection.md).

## Implemented behavior

The local `extract` command verifies a registered source hash, extracts one text record per PDF page, and writes a manifest recording the parser version, settings, source and output hashes, and limitations. It preserves document edition and provenance on each page. Empty pages are retained and flagged. Outputs are separate from originals; conflicting outputs are never overwritten.

The first run contains 12 sequential records, with no empty text pages. The source SHA-256 is `6de4c694b596d8c1246edc402de5efb9b3abb1e60a837e447c190f3b58c7a807`.

Output directory: [first extraction](../../data/processed/mars-007/6de4c694b596d8c1246edc402de5efb9b3abb1e60a837e447c190f3b58c7a807/04fc015a01c9ab9a1fc2f2406cbea383624cc73b937c24b57d7fbecc4b76624b/).

- [Page records](../../data/processed/mars-007/6de4c694b596d8c1246edc402de5efb9b3abb1e60a837e447c190f3b58c7a807/04fc015a01c9ab9a1fc2f2406cbea383624cc73b937c24b57d7fbecc4b76624b/pages.jsonl)
- [Extraction manifest](../../data/processed/mars-007/6de4c694b596d8c1246edc402de5efb9b3abb1e60a837e447c190f3b58c7a807/04fc015a01c9ab9a1fc2f2406cbea383624cc73b937c24b57d7fbecc4b76624b/manifest.json)

These generated artifacts are ignored by Git. They can be regenerated from the registered PDF and pinned parser. The code is [ingest.py](../../src/mars_rag/ingest.py); usage is documented in [the project README](../../README.md).

## Page numbering and visual checks

All 12 page footers were rendered and inspected. PDF position 1 has no visible printed page number; its `printed_page_label` is null. Positions 2-12 display printed labels 2-12, recorded as reviewed metadata in the source register. The PDF has no embedded `/PageLabels` dictionary, so `pdf_page_label` is null for all pages. Mandatory `pdf_page_number` remains 1-12 regardless of visible labels.

Full-page render checks cover pages 2, 3, 10, and 11, supplementing the earlier inspection of pages 1 and 4. Extraction sampling covers prose on pages 1-4 and 10-11. Page 3 retains the approximately 1,000-day/four-crew modeling assumptions, named maneuvers including return, and logistics categories. Pages 10-11 retain the discussion of cross-system tradeoffs, limitations, and conclusions. These checks establish sampled text usability, not complete scientific validation.

## Parser choice and limitations

The extraction extra pins `pypdf==6.21.4` while retaining the existing Python 3.9+ baseline. [Package metadata](https://pypi.org/project/pypdf/6.21.4/) identifies Python 3.9 compatibility. The [versioned text-extraction guidance](https://pypdf.readthedocs.io/en/6.21.4/user/extract-text.html) describes plain versus layout extraction and why PDF text needs checking.

Plain mode preserves page boundaries, but not visual layout. No automatic cleanup, OCR, table reconstruction, figure interpretation, chunking, embedding, retrieval, or answer generation is performed.

Observed limitations:

- Some words contain extra internal spaces or line breaks. Raw text is retained so later cleanup can be tested separately.
- Footers and footnotes can appear ahead of body text in the extracted reading order.
- Table 1 on page 2 is flattened; row/column relationships are not trusted as structured data.
- Diagram labels and chart content may be incomplete or detached from captions. Numeric answers from tables and plots require separate review.
- The source's exploratory assumptions remain essential context: its modeled mission is not an approved flight plan, and its total mission duration is not an outbound travel-time claim.

## Validation and next boundary

Eight automated tests use synthetic PDFs to check provenance, page separation and labels, empty pages, changed input hashes, unavailable or malformed sources, encryption, reruns, conflicts, and metadata revisions. Local validation uses Python 3.11; CI is configured to run the same tests on Python 3.9 and 3.11, but those remote jobs have not been run in this session.

Read-back checks confirmed all 12 records, label mappings, source/edition metadata, key prose on pages 2, 3, 10, and 11, an identical rerun, and all seven original PDF hashes. The output JSONL SHA-256 is `beb164589eddc0ccb364f2c456ebe0b4da5aa353306f635adff2e2224ddd7fb8`. Source and test files also passed Python 3.9 syntax parsing; Python 3.9 runtime execution was not available locally.

The next step is a reviewed evaluation set and simple retrieval against the extracted evidence. This extraction does not establish that search works, that a model can answer reliably, or that all source metadata and reuse questions are resolved.
