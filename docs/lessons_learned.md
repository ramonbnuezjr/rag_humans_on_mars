# Lessons learned while building the Mars research assistant

Started: 2026-11-22. This is a learning record, not a scientific review of Mars mission claims. Add concrete observations as the project develops; distinguish implemented behavior from proposals.

## What experience has taught us

| Observation | Lesson | Current behavior or limitation |
| --- | --- | --- |
| The question “Why does recycling water matter when packing food?” returned the life-support tradeoff discussion on PDF p. 6. | Retrieval can make a small, carefully chosen collection useful when the text addresses the question. | Five passages returned in the browser demonstration. This validates that example, not every future question. |
| “How would the crew of four being chosen for the trip to Mars?” returned trajectory dates “chosen,” rover capacity and other indirect matches. | Matching words does not establish matching intent. Five results do not mean five useful results. | The default is keyword BM25 search with full-page context. It does not assess whether evidence answers the question. |
| Existing extracted medical PDF p. 15 and DRA PDF p. 81 contain more relevant selection/composition discussion. | A poor result can reflect ranking failure even when useful evidence exists in the collection. | These are partial-evidence targets, not a verified selection procedure for a four-person Mars mission. DRA 5.0 describes a different, six-person concept. |
| Different papers assume different crew sizes and mission durations. | Source-grounded work must preserve assumptions as well as citations. | Mission notes and original-PDF links are displayed. Conflicting concepts are not automatically reconciled. |
| Short passages can omit nearby qualifications. | Inspect surrounding text before deciding what a passage supports. | Full-page context is expandable. It does not guarantee correct interpretation or complete evidence. |
| Experimental ranking improved some development examples but lost a maintenance-delay target in separate validation. | Improving known examples can introduce regressions. Preserve separate validation cases. | Experimental ranking remains optional; original ranking with page context is the default. |
| The page failed to load and a search reported “Failed to fetch” while no server was listening on port 8765. | A browser tab depends on a running backend. An operational failure is different from a retrieval-quality failure. | Restarting the server restored the page; the exact food/water question returned five passages. |
| Error capture requires a reachable server and writable disk. | Diagnostics have failure modes of their own. Confirm whether an event was actually saved. | Local errors show reference IDs and save status. No offline retry queue exists. |

## Owner ideas recorded: confidence and human feedback

Status: question-level human feedback is now implemented. Automatic coverage assessment, passage-level ratings, confidence percentages and automatic learning remain proposed. See [implementation and verification](research/2026-11-22-evidence-feedback.md).

The owner clarified that **whether the collection contains enough evidence for a complete answer is a central requirement**, not a secondary concern. Passage relevance alone is insufficient. Assess question-level coverage as well as relevance, source quality and mission applicability. A highly relevant passage may support only one part of a question.

The current BM25 score is a ranking value, not a probability. Converting it to a percentage or normalizing the top result to 100% would not establish correctness. Even several agreeing passages may repeat one source or describe incompatible mission concepts.

The owner requested an in-app choice rather than relying on chat-only feedback. Each successful search now offers **Fully**, **Partially**, **Not at all** or **Unsure**, plus an optional note. Save review intentionally persists the question and note with returned source/page/chunk identifiers, corpus/index references and retrieval code hash. Unsaved questions are not stored in the review database. PDF text is not copied. Error logs still exclude questions. Per-passage relevance controls remain proposed.

Initial feedback should build a reviewed evaluation set and record judgments about those specific question/passage pairs. It should not silently change global ranking or make a scientific claim more certain. Conflicting judgments and changed questions should remain visible. Any ranking change should be tested against separate cases before promotion.

Only after enough varied reviewed cases exist should we consider a numerical relevance estimate. Define a labeling rubric, reserve examples for calibration and untouched testing, and check whether passages assigned a given probability are actually judged relevant at approximately that frequency. Show sample size, uncertainty and limitations; do not invent a percentage for unfamiliar questions. Feedback used to tune a system cannot also be treated as independent proof of its quality.

The intended loop is **ask → assess evidence coverage → identify gaps → research those gaps → reassess**. Proposed coverage states are **supported**, **partially supported** and **insufficient evidence found**, each with citations, qualifications and a list of unresolved parts. These are judgments relative to a defined question and mission concept, not claims of universal completeness. Contradictions and unknown applicability must remain visible.

Before treating a failed answer as a collection gap, check whether relevant evidence was missed by retrieval. The crew-selection example exposed both a retrieval miss and an unresolved question: general selection/composition passages exist, but a specific four-person mission selection procedure has not been established. The first automatic label should therefore not assert that information is absent from the entire library based on five keyword matches.

Proposed feedback should capture both passage relevance and whether the evidence set answers the question completely, partially or inadequately. A research-gap record should retain the question, mission scope, supporting source/page references, unanswered parts, retrieval checks performed, candidate evidence needs and review status. Distinguish an owner-confirmed gap from an automated suggestion. A new source should trigger reassessment, not automatically close the gap.

Next use the implemented review controls on concrete questions to define the coverage rubric and gap-record format. Revisions persist, repeat submissions of the same choice/note for the same search do not create duplicate judgments, and the summary counts the latest rating per search. A fresh search is a new trial. User assessments are not independent scientific validation; changes in the mix of questions can change totals without improving retrieval. Comparing the same questions, mission scope and evidence versions is necessary to assess direction. Automated assessment, numerical confidence and automatic source acquisition remain unimplemented. Any numerical confidence later needs calibration against reviewed coverage judgments and a clear statement of what probability it represents.

## Supporting project records

A repeated [server outage on 2026-11-24](research/2026-11-24-server-outage.md) prevented both search and its error reporting. Confirmed no listener on port 8765; the termination cause is unknown. Recovery used a detached local process rather than another attached foreground tool session. Subsequent browser retry succeeded. This is operational recovery, not a retrieval improvement or an automatic restart service. Failures that cannot reach the diagnostic server are not present in its log and must not be claimed as captured.

On 2026-11-24 a [two-question diagnosis](research/2026-11-24-two-question-diagnosis.md) reproduced both owner misses exactly and showed why more PDFs alone would not fix them. Selection/composition evidence already existed at ranks 397 and 384; lunar-testing evidence was at rank 34. Rare words in unrelated contexts (chosen radiation cutoffs, launching through radiation belts) and incidental words such as “might” dominated the results. Clear diagnostic wording returned the relevant pages first without changing code. This proves an intent/terminology retrieval limitation on these cases, not a general fix or complete evidence. Missing selection procedures and a verified lunar-departure cost comparison remain separate research needs. The existing experimental ranking also misses the key targets for the original wording.

Owner testing found that placing the review form before the evidence interrupts reading. On 2026-11-23 the form was moved below all retrieved passages, following the flow question, evidence, then review. Two saved **Not at all** reviews concern crew selection and lunar departure infrastructure/costs. Their notes clarify the information need but do not prove the collection lacks the answer. Those retrieval issues remain open. See [owner review notes](research/2026-11-22-owner-review-notes.md). Capturing feedback and improving retrieval are separate milestones.

- [Retrieval ranking, comparison and validation](research/2026-11-21-ranking-review-and-comparison.md)
- [Local UI implementation and verification](research/2026-11-21-local-research-ui.md)
- [Local error log: verification and limits](research/2026-11-22-ui-error-log.md)
- [Architecture and current boundaries](architecture.md)

This record captures implementation observations and owner feedback. It does not add new mission evidence or replace review of the original PDFs.
