# Project status

Updated: 2026-11-24 (America/New_York).

## Stage

Local research UI and evidence retrieval. Nine original PDFs are registered; five are indexed, containing 267 pages and 993 page-bounded passages. Browser and CLI search work for one source or all registered indexes. A minimal chat-style local UI is implemented; generated answers, an insufficient-evidence classifier and voice are not. No embedding/generation provider is configured.

## Latest completed work

- Recovered a confirmed port-8765 outage on 2026-11-24 using a detached local server process with ignored startup log/PID files. The explicit crew-composition diagnostic question works again, returning five passages led by DRA PDF p. 81. These offline failures could not reach the diagnostic endpoint and are documented in the [outage record](docs/research/2026-11-24-server-outage.md), not represented as captured log entries. Why the previous process stopped is unconfirmed. No automatic startup/restart service or offline error queue was added.

- Completed the [two-question diagnosis](docs/research/2026-11-24-two-question-diagnosis.md). Both saved top-five result sets reproduce exactly. Selection evidence on medical PDF p. 15/DRA p. 81 ranks 397/384; lunar-testing evidence on DRA p. 90 ranks 34. Rare incidental words drive irrelevant matches; cost wording is unmatched. Explicit diagnostic queries retrieve useful existing pages first, while current experimental ranking still misses the principal targets for the original questions. Owned unindexed broad review p. 12 provides a depot lead, not a verified cost comparison. Specific selection tests and total lunar-versus-Earth cost remain candidate coverage gaps. Originals verified; no app, ranking, index, registry, ratings or collection changes made. Recommended next: a bounded, inspectable query-handling experiment with regression checks before source acquisition.

- Moved the evidence review survey after all returned passages on 2026-11-23, so assessment follows reading. Updated its wording and usage notes. Crew-selection and lunar-departure retrieval misses remain open; this changes placement only.

- Recorded [owner review notes](docs/research/2026-11-22-owner-review-notes.md): move the completeness prompt after the evidence (pending), and investigate two owner-rated Not at all results about crew selection and Moon departure infrastructure/cost. Browser placement and saved judgments were inspected directly. No placement/ranking fixes, additional papers or rating changes were made in this notes-only follow-up.

- Implemented owner-requested question-level feedback: Fully / Partially / Not at all / Unsure, optional note, explicit save confirmation and persistent local review summary. Signed search snapshots preserve evidence references and retrieval versions; edits retain history, retries do not double-count, and latest judgments count once per search. Questions/notes are intentionally saved locally only on review submission; the SQLite store is ignored by Git. Thirty-four tests pass plus browser save/revise/retry/reload checks using an isolated synthetic collection. See [feedback verification](docs/research/2026-11-22-evidence-feedback.md). Automated coverage, confidence, gap tracking and ranking adaptation remain unimplemented.

- Saved the [2026-11-22 project checkpoint](docs/research/2026-11-22-project-checkpoint.md), updated current architecture/source/evaluation/contribution guidance, and consolidated learning. Final local verification: 31 tests plus Python/JavaScript syntax checks pass; nine PDFs registered, five indexed. PDFs, generated outputs, diagnostics and environments remain outside Git.

- Saved the owner's clarified requirement: question-level evidence coverage is central. Planned supported/partial/insufficient assessments must identify unanswered parts and guide targeted research, while distinguishing retrieval misses from collection gaps. Human feedback should cover both relevance and completeness. These are documented requirements, not implemented capabilities; see [lessons learned](docs/lessons_learned.md) and [architecture](docs/architecture.md).

- Started a consolidated [lessons-learned record](docs/lessons_learned.md), connecting observed retrieval successes, misses, source assumptions and server failures to practical learning. Recorded owner ideas for confidence and human relevance feedback as proposals only. No scoring, feedback UI or automatic learning has been added.

- Added bounded local UI error logging with matching on-screen reference IDs, strict diagnostic fields, rotation and explicit save-failure feedback. Questions and PDF contents are excluded. Thirty-one software tests pass; browser checks verified server errors, network errors, unexpected JavaScript errors, unavailable logging and successful recovery. See [verification and limits](docs/research/2026-11-22-ui-error-log.md). Restart the existing server and reload to activate. Manual UX observations remain in the project conversation.

- Built the local research UI: question box, example prompts, in-tab thread/recent-search shortcuts, source filtering, optional experimental ranking, cited passages, complete-page expansion, source/mission caveats and original-PDF links. Each question remains an independent retrieval request.
- Added loopback-only standard-library HTTP serving with a fixed asset allowlist, request validation, origin/host checks and registered PDF hash/path checks. No new runtime dependencies, model calls or collection changes. Packaged HTML/CSS/JS verified in a built wheel.
- Twenty-seven software tests pass, including five synthetic-source HTTP integration tests. Browser checks covered search, filtering, context expansion, empty results, retry recovery and literal rendering of HTML-like query text. A composer overlap was found and fixed; viewport-based geometry confirms the conversation ends above it. Reliable phone viewport emulation was unavailable in the integrated browser; narrow-screen CSS is implemented but physical-phone validation remains pending.
- [Local UI implementation and verification](docs/research/2026-11-21-local-research-ui.md). Start with `.venv/bin/mars-rag serve`, then open http://127.0.0.1:8765. Preview servers used for testing are stopped after verification.

- Reviewed all six combined-search misses and added a preserved ranking comparison. Default search now returns exact complete-page context with unchanged original ranking; an experimental local query-hint/page/title reranker is available with `--ranking context`.
- Unchanged development targets: original/default 4/10, experimental 9/10 page-context hits (7/10 anchor hits). Separate frozen agent-authored validation: original 7/8, page default 8/8, experimental 7/8. Maintenance-delay regression prevents promoting experimental ranking. Integrated design remains a development miss. Two gap questions remain unscored; no answer-quality or sufficiency classifier exists.
- Twenty-two software tests pass; earlier eleven retrieval checks still pass. Original PDFs and immutable indexes remain unchanged. No new collection or generated answers added. See [review, demonstration and owner checks](docs/research/2026-11-21-ranking-review-and-comparison.md).

- Improved radiation prose using optional pinned pdfplumber/pdfminer extraction with geometric word spacing. All 65 pages retained; the rough long-token diagnostic fell from 561 to zero. Sampled PDF pp. 24, 44 and 46 checked visually. This does not validate every word, reading order, numerical tables or equations. Old extraction/index outputs and pointers are preserved.
- Added twelve realistic draft questions. Initial three-source results: 6/8 expected targets found at top five when source-scoped, 5/8 combined; four gap questions unscored.
- Added combined BM25 retrieval with corpus-wide statistics, index freshness checks and preserved source/page/edition/chunk provenance. CLI displays mission context, evidence type and review caveats.
- Targeted acquisition, registration, extraction and indexing of historical DRA 5.0 (100 PDF pages, 397 passages) and transit crew operations (11 pages, 41 passages). These address architecture and crew-activity coverage but describe distinct proposed mission concepts. Full source review remains pending.
- Expanded five-source results: 7/10 expected targets found at top five source-scoped, 4/10 combined; two gap questions remain unscored. The expanded set differs from the first set, so these ratios are not directly comparable. Narrow evidence targets are not complete relevance judgments or generated-answer grading. Combined ranking needs improvement.
- Eighteen software tests pass on Python 3.11. Python 3.9 syntax checked; the baseline remains Python 3.9+. CI is configured to install optional spacing support on Python 3.9/3.11; remote jobs were not run here.
- All nine original hashes, five index checksums, exact passage offsets and selected deterministic extraction/index reruns verified. Source PDFs and generated outputs remain excluded from Git. `CLAUDE.md` remains a relative symlink to `AGENTS.md`.

See [verification, results, source links and remaining work](docs/research/2026-11-21-retrieval-improvement-and-source-plan.md).

## Indexed sources

| ID | Scope | Pages | Passages |
| --- | --- | ---: | ---: |
| mars-004 | 2017 medical risk/evidence review | 79 | 217 |
| mars-006 | arXiv v2 radiation modeling/review | 65 | 284 |
| mars-007 | Exploratory life-support/transport tradeoffs | 12 | 54 |
| mars-008 | July 2009 DRA 5.0 reference architecture | 100 | 397 |
| mars-009 | SAC21 transit crew operations concept | 11 | 41 |

The broad mission/technology report (`mars-001`), oxygen-recovery development paper (`mars-005`) and distinct 2024/2021 Mars-GRAM guides (`mars-002`, `mars-003`) remain owned but unindexed. All nine sources remain pending full metadata/scientific/reuse review.

## Commands

```sh
.venv/bin/mars-rag serve
.venv/bin/mars-rag inventory
.venv/bin/mars-rag search all "Why does recycling water matter when packing food?" --top-k 5
.venv/bin/mars-rag search mars-007 "your question"
.venv/bin/mars-rag evaluate all
.venv/bin/python -m unittest discover -s tests -v
```

The realistic evaluation intentionally exits 1 while expected evidence targets are missed. Earlier source-specific checks remain available with `evaluate mars-004`, `evaluate mars-006`, or `evaluate mars-007`.

## Decisions and boundaries

- Display title: Humans on Mars; subtitle: A source-grounded RAG research project. Python package: `mars_rag`.
- Preserve originals, versions, provenance and source IDs. Keep different mission assumptions explicit; institutional authorship does not make proposals demonstrated capabilities.
- Local extraction, indexing and retrieval require no model/API calls or external document transfer. Downloading parser packages and two NASA PDFs did use the network. Provider choice and explicit content-transfer boundaries precede external embedding/generation.
- Medical report age remains an applicability caveat; no current treatment recommendations or safety certification established.
- No code license chosen; no Git push, publication or PR authorized.

## Next steps

1. Review three actual result pairs: integrated-design miss, maintenance-delay regression and mission-assumption success. Record acceptable support/qualifications before further tuning. Keep the original ranking with full-page context as default; collect fresh independent review questions before considering promotion of experimental reranking.
2. Review source-specific mission assumptions and adjacent pages; validate only the numerical tables needed for selected questions. Improve metadata/reuse records and verify contemporary evidence before current medical or safety claims.
3. Resolve remaining coverage gaps selectively: detailed interior layout, individual duties and actual Mars daily schedules remain unestablished; puncture repair procedures and governance lack dedicated support. Inspect owned sources before acquiring more.
4. Use the new review controls on a small set of real questions to define a question-level coverage rubric and research-gap record, starting with crew selection. Include mission assumptions, citations and checks for retrieval misses. Manual feedback storage is implemented; automatic classification and numerical confidence are not. Compare repeated questions and evidence versions, not changing aggregate counts alone.
5. Choose answer generation/provider and data-transfer boundaries after evidence retrieval is sufficiently reliable. Evaluate citation support, coverage and uncertainty before generated answers or voice; the retrieval-only local UI is already implemented.

## Earlier records

- [Radiation/medical processing and initial coverage](docs/research/2026-11-21-radiation-medical-processing-and-coverage.md).
- [First index and retrieval verification](docs/research/2026-11-21-local-index-and-retrieval.md).
- [First page-preserving extraction](docs/research/2026-11-21-page-preserving-extraction.md).
- [Initial four-PDF inspection](docs/research/2026-11-21-initial-pdf-inspection.md).
- [Preliminary Earth-to-Mars synthesis](docs/research/2026-11-19-earth-to-mars-overview.md) and [follow-up questions](docs/research/2026-11-19-earth-to-mars-follow-up-questions.md).
- [Research map/workflow](docs/research/2026-11-19-research-map-and-rag-workflow.md) and [research tools/source discovery](docs/research/2026-11-21-research-tools-and-source-discovery.md).

## Deferred

Bulk acquisition, automated crawling, hosted databases, agents, fine-tuning, remote deployment, generated answers and voice.
