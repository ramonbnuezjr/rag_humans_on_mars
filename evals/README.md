# Research evaluations

`questions.jsonl` contains draft questions, not a scored benchmark. None has been checked against the initial PDFs. An empty evidence list means “not reviewed,” not “the corpus has no answer.”

For each reviewed question, record supporting source IDs, exact PDF page numbers, and a short expected finding. Include answerable questions, questions outside the collection, and questions that need evidence from multiple sources or conflicting editions.

Only label a question as unanswerable after checking the indexed collection. When retrieval exists, measure whether known evidence is returned in the top-k passages. When generation exists, separately assess whether claims and citations are supported. Record the corpus snapshot and retrieval/model settings with results in `results/`.

## Evidence coverage and human review: planned

The owner requires question-level judgments of whether the evidence supports a complete answer, only a partial answer, or is insufficient. Passage relevance alone cannot establish this. Define a scoped rubric, list supporting citations and unanswered parts, check for retrieval misses before recommending new sources, and record human review separately from an automated suggestion. The crew-selection question is a concrete example: the UI returned indirect word matches, while existing extracted medical PDF p. 15 and DRA PDF p. 81 provide partial selection/composition evidence. They do not establish a specific four-person mission's selection procedure.

Manual question-level feedback is implemented and stored locally with the question, returned evidence references and retrieval versions. Automated coverage assessment, research-gap tracking and calibrated confidence are not implemented or scored by the existing evaluations. BM25 scores and top-k page hits are not completeness probabilities. Owner reviews do not automatically become benchmark labels. Compare the same scoped questions and preserve review provenance; feedback used for tuning must be separated from independent testing. See [lessons learned](../docs/lessons_learned.md).

## Current retrieval development cases

The three source-specific retrieval files retain eleven earlier checks. `research-retrieval-v1-three-source.jsonl` preserves the initial twelve realistic questions and their three-source scope. `research-retrieval.jsonl` is the expanded, draft agent-reviewed version: ten version-bound expected-evidence targets (some explicitly partial) and two unscored gap questions. It does not replace the original `questions.jsonl`.

Run `.venv/bin/mars-rag evaluate all` to measure combined retrieval on all active registered indexes. Missed evidence targets produce exit status 1; this is a measured retrieval limitation, not a failed software unit test. Gap cases print REVIEW and cannot count as abstention successes. The generated report records the dataset checksum and active source/index snapshot. Source-scoped comparison is available through `evaluate_research(root, combined=False)` in the evaluation module.

## Ranking comparisons

`ranking-validation.jsonl` contains eight additional draft agent-authored questions frozen before candidate experiments. They are separate from the development set, but not independently reviewed or blind; they informed the default-selection decision and are now consumed validation data. Further tuning needs fresh checks.

Use `evaluate all --ranking baseline|page|context` and optionally `--eval-set ranking-validation.jsonl`. The page default preserves original ranking while returning full pages. Experimental context ranking is opt-in. Reports explicitly distinguish full-page support from short-anchor support; two development gap cases remain unscored. Do not interpret larger-context hits as an equal increase in ranking accuracy.
