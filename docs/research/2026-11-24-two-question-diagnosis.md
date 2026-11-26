# Diagnosis: crew selection and lunar departure

Date: 2026-11-24. Local investigation only. No application, ranking, registry, extraction pointers, indexes, source PDFs or saved owner ratings were changed. No new documents were downloaded.

## Finding and decision

**Both questions expose retrieval failures and remaining evidence gaps. Adding documents alone would not solve the demonstrated failures.** Relevant partial evidence is already indexed but ranks below the displayed top five. Neither the displayed results nor the inspected supporting material establish the complete answers the owner wants.

Recommended next implementation milestone: test an optional local intent/query-expansion approach against these original questions and the existing regression checks. Preserve the original wording and include diagnostic expansions in the evidence record. Do not promote the existing experimental reranker: it also misses the key pages for these two questions. Do not add answer generation or bulk acquisition as a response to this diagnosis.

## What was checked

- Read the two latest saved owner reviews and their signed search snapshots. Both are rated **Not at all**.
- Verified the nine original PDF hashes against the register and loaded all five active indexes/extractions through existing integrity checks: 267 pages, 993 chunks.
- Reproduced the original default searches. All five returned chunk IDs matched each saved search exactly. This is a relevance failure, not a different run or an unavailable-server symptom.
- Computed BM25 contributions by query term and best chunk rank per candidate page across all matching chunks. Ranks below are chunk ranks, not unique-page ranks; lower numbers are better.
- Read complete candidate pages. Visually checked original DRA PDF pp. 17, 81 and 90 and the broad technology review PDF p. 12.
- Screened all four owned but unindexed PDFs locally using temporary pypdf text: broad technology review 18 pages, two Mars-GRAM guides 81 pages each, oxygen-recovery paper 12 pages. Used crew/selection/psychology and lunar/Moon terms, then inspected promising context. This was not a scientific review of every page or OCR of figures, so “not found” is not proof of absence. No production extraction/index was created.

Detailed search snapshots, target ranks, per-term contributions, diagnostic query results and scratch text are saved in ignored `evals/results/2026-11-24-two-question-diagnosis.json`. Rendered checks are in ignored `evals/results/diagnosis-pages/`. They remain local, outside Git.

## 1. How are the four astronauts chosen for the mission to Mars?

Owner intent: screening/tests, psychological suitability, extreme-stress performance, team selection and possible relevance of military experience.

### Failure demonstrated

The default searches the words `four`, `astronauts`, `chosen`, `mission`, `mars`. It does not translate “chosen” into “selection,” “screening” or “crew composition.” In the 993-chunk corpus, `chosen` occurs in only 19 chunks, making an incidental match influential.

The first result, radiation PDF p. 50, scores **13.205**. Its word contributions are chosen 4.153, four 3.646, astronauts 3.031, mission 1.301 and Mars 1.074. In context, these refer to radiation cutoffs and a follow-up interval of several decades, not selection of four people. The second result matches dates chosen for a trajectory study; the third matches a chosen site and rover contingency capacity. The ranker does not understand the relationship between “four,” “astronauts” and “chosen.”

### Useful existing evidence and limits

| Supporting source | Default best chunk rank | What it supports | What it does not establish |
| --- | ---: | --- | --- |
| [Medical risk report](../../data/raw/20170004604.pdf), PDF p. 15 | 397 | Fair selection, mission suitability and informed understanding of risks, as discussed in a 2017 medical/ethical review. | A psychological test battery, decision thresholds or the selection process for a specific four-person mission. |
| [DRA 5.0](../../data/raw/373665main_nasa-sp-2009-566.pdf), PDF p. 81, section 7.1.5 | 384 | Personal/interpersonal characteristics, team functioning, skill mix, isolation/stress and proposed studies in simulations/analogs. | Operationally validated selection criteria. This is a historical 2009 **six-person** reference concept; its proposals cannot be relabeled as an approved four-person process. |

Medical PDF p. 36 also discusses cross-training and simulation for clinical/team skills, but training is not evidence of an admission or selection test. Neither military priority nor a military requirement was established in the inspected evidence. The owner's suggestion remains a research question.

**Diagnosis:** confirmed retrieval miss for available partial selection/composition evidence; a candidate coverage gap for the specific tests, thresholds, staffing/selection authority and actual four-person mission procedure. Define the intended mission concept before treating all selection requirements as interchangeable.

## 2. Launching from Earth might be costly. Would we launch from the Moon?

Owner intent: lunar infrastructure as a Mars departure base, lunar preparation/training and total cost relative to Earth departure. These are related but distinct questions.

### Failure demonstrated

`costly` occurs in **zero** indexed chunks, so the cost part receives no matching contribution. `launching` occurs in only **one** chunk, giving the radiation-belts passage a 6.695-point contribution from that word alone. The words `might` and `we` remain searchable despite being incidental to the information need.

The first result, DRA PDF p. 93, scores **9.532** entirely from `moon` (5.413) and `might` (4.118, rounding explains the sum). It discusses public/cultural perspectives and has no contribution from launch or cost terms. The app has no intent or evidence-coverage check to reject this result as an answer to an infrastructure/cost comparison.

### Useful existing evidence and limits

| Supporting source | Default best chunk rank | What it supports | What it does not establish |
| --- | ---: | --- | --- |
| [DRA 5.0](../../data/raw/373665main_nasa-sp-2009-566.pdf), PDF p. 90, continuation of section 7.5.2 from p. 89 | 34 | Proposed lunar testing of Mars-relevant equipment, crew adaptability, operations, reliability, maintenance, habitats, rovers, power and local resource use. | A completed lunar proving program, a lunar Mars launch base, or measured cost savings. |
| DRA 5.0, PDF p. 17 | 47 | The reference concept launches mission elements from Earth, docks/checks them in low Earth orbit and departs from Earth orbit. | That all future Mars missions must follow this architecture. “Lunar cargo launch vehicle” describes its vehicle/program role, not a launch site on the Moon. |
| [Approaches To Humans-Mars Both Safe and Affordable](<../../data/raw/Approaches To Humans-Mars Both Safe and Affordable.pdf>), PDF p. 12 | Not indexed | A depot proposal considers fuel from Earth, Moon, Mars or asteroids and identifies sourcing, production, transport, storage and dispensing as system elements. | A verified end-to-end comparison proving lunar departure cheaper. It is a broad 2022 technology/proposal review with speculative content; p. 11 also flags resource/business-case uncertainty. |

The second displayed result, DRA PDF p. 16, already provides some precursor-testing context, but not the detailed infrastructure or cost answer. The unindexed broad review is an owned lead, not a reason to assume the answer is complete after indexing it. The two atmospheric model guides and oxygen-recovery paper did not reveal a better targeted selection or lunar-departure cost study in this text screening.

**Diagnosis:** confirmed retrieval miss for lunar testing and Earth-orbit departure evidence; an indexing exclusion for an owned depot discussion; a candidate evidence gap for a comparable, assumption-explicit total-cost study. Lunar testing, lunar-sourced fuel and launch from the lunar surface must not be combined into one established architecture. The owner's cheaper-lunar-launch assumption remains unverified.

## Diagnostic demonstrations: evidence is retrievable

These explicit questions were run through the **unchanged default** method. They are diagnostic probes informed by inspected pages, not independent validation or a fix the owner must supply manually.

| Diagnostic wording | First result |
| --- | --- |
| What personal and interpersonal characteristics, skill mix and psychological factors should guide crew composition and selection? | DRA PDF p. 81; medical p. 15 also appears in the top five. |
| How could lunar missions test Mars hardware, crew adaptability, maintenance and ISRU before a Mars mission? | DRA PDF p. 90. |
| Where are Mars mission vehicles launched, assembled and checked out before departure from Earth orbit? | DRA PDF p. 17. |

The existing experimental `context` mode was also checked with both **original** questions. It still does not return the principal crew-selection or lunar-testing pages in the top five. Turning that option on is not a demonstrated remedy. Full-page expansion does not rescue a useful page that was never selected.

## Smallest useful next step and completion criteria

1. Preserve the original two questions, owner notes and partial-evidence targets as development cases. These cases are already inspected and must not be presented as blind evaluation.
2. Prototype explicit, inspectable query intent/terminology handling locally. Keep mission specificity and the original question visible; do not hard-code source/page answers or silently erase the four-person qualifier. A multi-part lunar question may need separate retrieval for proving-ground, departure and cost evidence.
3. Compare original versus candidate results for these cases and previously successful food/water, maintenance-delay, medical and radiation questions. Check regressions and obtain fresh review before promotion.
4. Report the result as either improved evidence retrieval or a remaining miss. Even if partial evidence becomes easy to find, retain an explicit completeness gap for selection procedures and lunar cost comparison. Only then select dedicated sources to fill those named gaps.

This investigation is complete when the cause and evidence boundaries are reviewable. That condition is met here. Retrieval improvement, new acquisition and automated sufficiency judgments have **not** been implemented or validated by this report.
