# Local index and retrieval verification

Date: 2026-11-21 (America/New_York)

Scope: Index and search the verified extraction of `mars-007`, the life-support tradeoff paper. No additional PDF acquisition, embeddings, model calls, generated answers, web interface, or voice functionality was added.

## Implemented result

The 12-page extraction produces 54 overlapping passages. Each passage stays within one page and retains source/edition/hash metadata, extraction ID, exact text offsets, and page labels. BM25 ranks keyword matches over a local inverted index. The source register now marks only this source as indexed and selects its current index; scientific metadata review remains pending.

- [Index output directory](../../data/index/mars-007/2430341304bba82bed5c28903b90570fab3e4b5409e09e4814adaabc7e280353/)
- [Index manifest](../../data/index/mars-007/2430341304bba82bed5c28903b90570fab3e4b5409e09e4814adaabc7e280353/manifest.json)
- [Index data including passages](../../data/index/mars-007/2430341304bba82bed5c28903b90570fab3e4b5409e09e4814adaabc7e280353/index.json)
- [Provisional development cases](../../evals/mars-007-retrieval.jsonl)
- [Evaluation result](../../evals/results/mars-007-ef03454b7994e98bc0f1fdbcd19e9fb996c0db25613f6b6754630a163b2162cd.json)

Generated index and evaluation result files remain ignored by Git. The original draft evaluation questions are unchanged. These development cases were selected from previously inspected passages before the first index run; they have not received independent human review and are not a held-out benchmark.

## Reproduction

From the repository root with the project installed:

```sh
.venv/bin/mars-rag index mars-007
.venv/bin/mars-rag search mars-007 "Why does food hydration affect water recycling choices?" --top-k 3
.venv/bin/mars-rag evaluate mars-007
```

Index settings: 180-word chunks, 30-word overlap, no crossing pages, lowercase alphanumeric tokenization with a fixed stop list, no stemming or synonyms, BM25 `k1=1.2` and `b=0.75`. Raw extraction is unchanged; whitespace normalization is used only when checking expected phrases in the evaluation.

## Initial retrieval checks

An evidence case passes if at least one of the first five returned chunks contains both an expected PDF page number and its specified supporting phrase. This is a minimal evidence-location check, not entailment grading or completeness scoring.

| Development question | Expected PDF page | First matching support rank |
| --- | --- | --- |
| Baseline crew size and mission duration | 3 | 2 |
| Supplies in the logistics model | 3 | 2 |
| Propulsion consequences of isolated ECLSS optimization | 10 | 1 |
| Food hydration and water recycling choices | 10 | 3 |
| Future habitat sizing and power/thermal modeling | 11 | 1 |

All five expected evidence passages occur within the first five results. Two occur first; mean reciprocal rank at five is approximately 0.667. The captain probe returns no keyword matches. The latter only demonstrates lexical no-match behavior; it is not a general absence-of-evidence classifier.

For the food/water question, the search also returns relevant prose on page 6 before the expected page-10 passage. The narrow development labels are not an exhaustive relevance judgment. Do not interpret every non-target result as irrelevant or treat these six cases as proof of broad retrieval quality.

## Software and preservation checks

Fourteen automated tests use synthetic PDFs to cover extraction and index behavior, including page/offset preservation, distinct labels, source version handling, input/output checksums, reruns, ranking, and CLI/evaluation integration. Tests run locally on Python 3.11. Python 3.9 runtime execution and remote CI remain unverified; the existing Python 3.9/3.11 CI matrix runs synthetic tests without private source files.

The indexer verifies original and extraction hashes before building. Search checks input freshness and index checksums. Identical rebuilds reuse output; conflicts are rejected without replacement. No PDF or extraction page record was changed by indexing.

## Limits and next work

- Only `mars-007` is searched. The other six registered PDFs remain unindexed.
- Keyword matching can miss paraphrases and rank shared terminology above actual support. Scores are not confidence values.
- Passages include flattened technical content and references; tables, plots, equations, and cross-page arguments need human inspection.
- A matching passage can omit a caveat elsewhere in the paper. Keep its exploratory mission assumptions and consult surrounding evidence.
- No-answer behavior currently means no matching terms, not a reliable judgment that the library cannot answer a question.

The next milestone is to inspect additional question/results pairs and improve the evaluation set, then assess whether the baseline needs different chunking, query handling, or semantic retrieval. Provider choice and external data-transfer decisions precede any hosted embedding or answer-generation service.
