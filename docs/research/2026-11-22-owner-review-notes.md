# Owner review notes — 2026-11-22

Status: observations recorded for follow-up. No UI placement or ranking changes made in response to these notes.

Update 2026-11-23: the review form has now been moved after all returned passages, following the owner's request. The retrieval-quality investigations below remain open.

Update 2026-11-24: [diagnosis completed](2026-11-24-two-question-diagnosis.md). Confirmed retrieval misses coexist with remaining partial-evidence gaps; ranking/collection remediation remains pending. The original observations below are retained as history.

## UX: evidence before evaluation

The owner reports that the feedback question appears before the evidence has been read. This interrupts the reading sequence and makes the retrieved material feel secondary to the review form. Browser inspection confirms that the form currently precedes the result cards.

Desired sequence: question → retrieved evidence → completeness choice and optional note. Moving the form below all returned passages is a documented follow-up, not an implemented fix. Keeping feedback discoverable should not require displaying the full review form before the material being reviewed.

## Saved retrieval feedback

The following latest reviews were read directly from the local review store. Both were explicitly rated **Not at all** by the owner. These are judgments about whether returned evidence meets the information need, not automatic scientific or corpus-wide completeness labels.

| Question | Owner's intended information need | Returned source/PDF pages | Follow-up |
| --- | --- | --- | --- |
| How are the four astronauts chosen for the mission to Mars? | Specific screening/tests, psychological profile, ability to manage extreme stress and make decisions, and whether military experience would be relevant. | mars-006 pp. 50, 5; mars-008 pp. 35, 54; mars-009 p. 9 | Review relevant owned evidence and diagnose ranking versus collection coverage. No specific four-person mission concept or selection procedure has been established. |
| Launching from Earth might be costly. Would we launch from the Moon? | Whether lunar infrastructure could support departure to Mars, whether the Moon could be a training ground, and a comparison of the costs of lunar and Earth departure architectures. | mars-008 pp. 93, 16, 21, 27; mars-006 p. 3 | Distinguish lunar training/testing from using the Moon as a departure base, then investigate architecture/evidence coverage. The first displayed passage concerns cultural/public perspectives, not the requested infrastructure/cost comparison. |

The owner raised military participation and cheaper lunar launching as possibilities/assumptions to investigate. Neither is established by these reviews. In particular, no full-system cost comparison was verified, and the identity or selection policy of a future Mars crew is not established here.

Existing partial discussion of lunar testing or crew selection does not establish a complete answer. Further evidence inspection is needed before declaring either a confirmed collection gap or a ranking-only problem. Saved reviews remain unchanged in the local database; these notes do not create new ratings, download sources or alter retrieval behavior.

## Learning

Feedback is already useful: it captures the distinction between word matches and the owner's actual question, including unresolved subquestions. Capturing it does not itself improve retrieval. Track observed misses separately from completed fixes and reassess the same questions after a deliberate change.

Related: [feedback implementation](2026-11-22-evidence-feedback.md), [lessons learned](../lessons_learned.md), [current status](../../status.md).
