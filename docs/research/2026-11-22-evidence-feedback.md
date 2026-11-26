# Evidence coverage feedback — 2026-11-22

The owner requested in-app judgments of whether returned evidence answers the question: Fully, Partially, Not at all or Unsure. Manual feedback is now implemented; no automated completeness classification, confidence percentage or ranking change is implied.

## Use

Ask a question. Review the returned passages, choose an assessment in the review form after the last passage, optionally explain what remains missing or useful, then select Save review. The form confirms saving or preserves inputs and reports failure. Change the choice/note and save again to revise that search's review. An empty-result search can also be reviewed; failed searches cannot. Placement was corrected on 2026-11-23 following owner feedback.

Saved evidence reviews in the desktop sidebar shows latest counts and five recent reviewed questions; expand an entry to inspect the note and timestamp. Thread history still clears on reload, but saved reviews persist. Narrow-screen CSS hides the sidebar summary alongside the existing sidebar content; per-search review controls remain available. The complete record is stored locally and has no dedicated export/history editor yet.

## Persistence and boundaries

[Feedback storage](../../src/mars_rag/feedback.py) uses standard-library SQLite in ignored `feedback/reviews.sqlite3`. Only explicit Save review persists a question. Each review includes the exact question, rating/note/timestamps and a signed snapshot containing search ID, source filter, corpus/index references, returned source/page/chunk IDs and a retrieval code hash. PDF passages are not copied. A local persistent signing key prevents submitting altered search references. Unsaved search snapshots live in the response/tab only; the database can exist to hold the signing key even with zero reviews. Storage failure does not hide successful retrieval results.

Each edit adds a retained revision. Repeating the same save for the same search/rating/note reuses its receipt, preventing double-counting after a retry. Summary counts use only each search's latest judgment. A fresh search has a different ID, even for identical wording, allowing later comparisons. The UI does not automatically reload saved choices onto a new search. Feedback contents and the signing key are excluded from Git and served only through the loopback summary endpoint, not as downloadable project files. Error logs still exclude questions/notes.

## Verification

34 software tests pass. New checks cover storage reopening, all four choices, exact provenance, idempotent retries, revision history, latest counts, malformed/altered receipts, cross-origin rejection, no-match evidence and storage failure. Python compilation and JavaScript syntax checks pass.

An isolated two-page synthetic collection on port 8766 was used for browser QA, keeping fake judgments outside the owner's actual collection. Partially saved as one reviewed search; revising to Fully kept one search and removed its old count. A blocked feedback POST showed “Review not saved,” preserved Unsure and the note, and allowed retry. Unsure then persisted after reload. No confidence or scientific accuracy claims were generated from these examples.

## What this tells us

The review record captures whether the evidence met the owner's information need and what was missing. It is not independent source validation. Aggregate ratings can change because different questions were asked; they do not prove improving or declining accuracy. Review the same questions and mission scopes against preserved corpus/retrieval versions to assess progress, and investigate retrieval misses before acquiring more material. Automatic research-gap classification, recommendations, benchmark promotion, learning and feedback-driven ranking are future work.
