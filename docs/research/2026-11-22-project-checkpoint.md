# Project checkpoint — 2026-11-22

## Implemented and verified locally

The MVP provides local PDF evidence search through a minimal browser interface and CLI. Nine PDFs are registered; five have active page-preserving extractions and indexes (267 PDF pages, 993 passages). Default search preserves BM25 order and includes full-page context. Source IDs, editions, page references and processing identifiers remain inspectable. Experimental ranking is opt-in because validation showed a regression.

The UI restores failed questions for retry. Bounded, local diagnostic logging captures server errors and browser reports with matching reference IDs; question text and PDF contents are excluded. Other UX observations are reported in the project conversation. A server outage was confirmed by the absence of a listener on port 8765; restarting restored the page. The existing app server was left running after recovery, but is not installed as an automatic startup service.

Final local checks: 31 software tests pass, Python compilation passes, JavaScript syntax passes, and inventory reports nine registered PDFs with five marked indexed. Inventory alone does not verify hashes or index integrity. The software suite uses synthetic fixtures. The water/food question was verified in the live browser and returned five passages, led by the life-support paper's PDF p. 6. These results do not establish general answer accuracy.

## Owner decisions and limitations

- The owner considers this a useful MVP and accepts that detailed questions expose gaps.
- A crew-selection question exposed indirect keyword matches. Existing medical PDF p. 15 and DRA PDF p. 81 contain partial evidence, but no specific four-person Mars selection procedure has been established. The DRA concept uses six crew; assumptions must remain distinct.
- Evidence coverage is central: the intended assistant should identify whether it can answer the whole question, only part of it, or has insufficient evidence, then state specific evidence needs.
- Human feedback should address both passage relevance and question-level completeness. BM25 values are not confidence percentages. Numerical confidence needs a defined target and calibration against reviewed examples.
- Before recommending acquisition, investigate whether retrieval missed material already owned. The planned loop is ask, assess coverage, identify gaps, research them and reassess.

Generated answers, automated evidence-coverage judgments, a persistent research-gap register, feedback controls, calibrated confidence, web research/acquisition and voice remain unimplemented. No provider is configured. No new papers or source-content changes were made during this checkpoint.

## Next design work

Define a coverage rubric and a reviewable gap-record format using real questions. Include mission scope, cited support, unresolved parts, retrieval checks and owner review. Select provider/data-transfer boundaries before implementing external generation. Source metadata, scientific applicability and reuse reviews remain pending.

## Git boundary

The requested repository is [ramonbnuezjr/rag_humans_on_mars](https://github.com/ramonbnuezjr/rag_humans_on_mars). It was confirmed empty before the first project commit was prepared. Commit code, documentation, registry metadata and small evaluation definitions; keep PDFs, generated text/indexes/results, diagnostics, environments and credentials local. Preserve `CLAUDE.md` as a relative symlink to `AGENTS.md`. No code license has been selected.

## Related records

- [Current status](../../status.md)
- [Lessons learned](../lessons_learned.md)
- [Architecture and planned coverage loop](../architecture.md)
- [Error logging verification](2026-11-22-ui-error-log.md)
- [Retrieval ranking comparison](2026-11-21-ranking-review-and-comparison.md)
