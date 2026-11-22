# Inspection of four newly added PDFs

Date: 2026-11-21 (America/New_York)

Status: Preliminary source inspection and MVP recommendation. This is a sampled review, not a complete scientific validation or a synthesis into one mission architecture.

## Result

The four additions are relevant technical sources on medical care, oxygen recovery, radiation, and integrated life-support design. They provide enough material to begin a narrow extraction and retrieval experiment. They do not, based on the reviewed sections, establish a complete launch-to-arrival mission, crew roster, daily schedule, or settled vehicle design.

All four open successfully, are unencrypted, and yield text on every page: 168 pages total. First pages and one representative technical page per file were rendered and visually inspected. Text presence alone is not proof of correct reading order or table extraction. The original PDFs were not edited. No remote PDFs were downloaded; NASA NTRS and arXiv landing-page records were consulted for provenance.

The [source register](../../sources/registry.json) now includes seven records. The three original entries were preserved; the four additions remain `needs_review` and `not_indexed`. Content-based title and author matching supports source identity, but local files were not byte-compared with remote copies. Local hashes identify the inspected artifacts.

## Sources and relevance

### Medical care and autonomy

- Local source: [20170004604.pdf](../../data/raw/20170004604.pdf), `mars-004`, 79 PDF pages.
- Title: Risk of Adverse Health Outcomes and Decrements in Performance due to In-Flight Medical Conditions.
- Provenance: [NASA NTRS record 20170004604](https://ntrs.nasa.gov/citations/20170004604), catalog publication date 2017-01-01. NTRS lists Erik Antonsen; the PDF lists multiple current and previous contributors. Its cover retains a public-release date placeholder, so the cover is not evidence of a completed release date. NTRS separately identifies the record as public.
- Evidence type: evidence review and medical-risk analysis; recommendations must retain their 2017 context.
- Reviewed sections: PDF pages 1-5 and 10-13, including contents, executive summary, habitat constraints, communication and evacuation constraints, and the need for a medical concept of operations.
- Useful questions: Why does medical care need greater autonomy? How do mass, volume, communication delay, and evacuation limits affect onboard medicine?
- Extraction finding: Coordinate-sorted text merges words and headings in the sampled prose. Original PDF text order produces substantially better spacing on page 10. Do not treat this as an OCR-only document or assume one global sorting setting is safe.
- Review limits: Not a crew medical protocol, current policy, or complete mission plan. Specific medical recommendations and numeric communication assumptions require current corroboration before broader use.

### Oxygen recovery technology

- Local source: [20200003267.pdf](../../data/raw/20200003267.pdf), `mars-005`, 12 PDF pages.
- Title: Developmental Efforts of an Electrochemical Oxygen Recovery System for Advanced Life Support.
- Provenance: [NASA NTRS record 20200003267](https://ntrs.nasa.gov/citations/20200003267), publication date 2020-07-12; ICES-2020-74. The title page lists Brittany R. Brown and seven coauthors. Brian Dennis and Wilaiwan Chanmanee appear in the PDF author list but not the shorter NTRS list; the register follows the PDF.
- Evidence type: technology development and laboratory experimentation. Do not promote proposed advantages to demonstrated operational performance.
- Reviewed sections: PDF pages 1, 2, 8, 10, and 11, covering the abstract, recovery pathway, electrolyte table, test results, and cell-design optimization.
- Useful questions: What is this reactor intended to replace? How does the described oxygen-recovery pathway work? Which scaling and material-selection issues were still under investigation?
- Extraction finding: Prose is mostly usable. Chemical subscripts, equations, table row relationships, figure labels, and graph axes require separate checks. Text near figures can be detached from its intended reading order.
- Review limits: Historical development results do not establish present deployment or a flight-qualified Mars system. The 3D-printed apparatus mentioned on page 10 is a laboratory test setup, not evidence of an onboard manufacturing capability.

### Radiation exposure and shielding

- Local source: [2208.00892v2.pdf](../../data/raw/2208.00892v2.pdf), `mars-006`, 65 PDF pages.
- Title: Crewed Missions to Mars: Modeling the Impact of Astrophysical Charged Particles on Astronauts and Their Health.
- Provenance: [arXiv record 2208.00892](https://arxiv.org/abs/2208.00892). Local title page and arXiv history identify v2, submitted 2023-01-05; the initial version was submitted 2022-08-01. The record says “Under Review”; journal publication and peer-review outcome were not verified.
- Evidence type: numerical radiation modeling plus literature review. Computed organ doses are modeled estimates, not measurements from an actual crewed Mars journey.
- Reviewed sections: PDF pages 1-3, 24, 27, and 50, including abstract, scope, methods, an organ-dose table, and mitigation discussion.
- Useful questions: Which radiation populations and scenarios are modeled? What shielding assumptions apply? What limitations prevent using a table value as a universal crew exposure prediction?
- Extraction finding: First-page margin text and affiliations interrupt sorted reading order. Page 27 contains a dense multilevel numerical table; plain extracted text is insufficient to trust row/column associations, scenario labels, and units.
- Model boundary: Page 24 describes GEANT4, human phantoms, no-shield and aluminum-shield scenarios, solar conditions, and a simplifying omission of minor heavier GCR species. Carry these assumptions with any resulting claim. Medical mitigation suggestions are not validated treatment recommendations.
- Review limits: License and publication status remain unresolved; do not claim that any reviewed mitigation eliminates radiation risk.

### Life support and mission tradeoffs

- Local source: [ECLSS Does Not Exist in a Vacuum v9 (unlinked citations).pdf](<../../data/raw/ECLSS Does Not Exist in a Vacuum v9 (unlinked citations).pdf>), `mars-007`, 12 PDF pages.
- Title: ECLSS Does Not Exist in a Vacuum: Integrated Analysis is Necessary to Inform System Architecture Decisions.
- Provenance: [NASA NTRS record 20205001088](https://ntrs.nasa.gov/citations/20205001088). Andrew C. Owens and eight coauthors. The paper header says ICES-2020-310; the catalog report field says CES-2020-310. The local filename says v9, which is retained as a local version label, not independently established publication history.
- Evidence type: exploratory system modeling. Page 2 explicitly says the scenarios are not implementation plans.
- Reviewed sections: PDF pages 1-4 and 10-11, including motivation, assumptions, logistics categories, transportation model, limitations, and conclusions.
- Useful questions: How do recycling, food water content, spares, and propulsion affect each other? Why might a lighter subsystem fail to produce the best overall mission?
- Extraction finding: Sampled prose is suitable for a first retrieval experiment. Acronym tables, the architecture matrix, and plotted results need structural handling or exclusion from initial numeric evaluation.
- Mission boundary: PDF page 3 assumes approximately 1,000 days and four crew for a conjunction-class mission including return. This is not a 1,000-day Earth-to-Mars transit claim. Page 4 uses a hybrid chemical/solar-electric propulsion model. These are this study's assumptions, not a selected project baseline or facts about every Mars mission.
- Review limits: Publication date and actual conference presentation status are not established. The PDF declares US Government work, while NTRS uses narrower reuse wording; redistribution terms need reconciliation. Page 11 identifies unmodeled or future work, including changes in habitat sizing and power/thermal modeling.

## Recommended first experiment

Start with `mars-007` and its prose on PDF pages 1-4 and 10-11. It is short, connects several of the owner's interests, and makes its modeling boundaries explicit. Pairing it later with the medical report can broaden coverage without mixing their mission assumptions.

The recommendation is to test evidence retrieval before generated answers. The questions below are reviewer-proposed candidates, not scored evaluations. Page references are one-based PDF positions; confirm printed labels when creating production evidence records.

| Candidate question | Expected supporting evidence in mars-007 |
| --- | --- |
| Why must life-support decisions be evaluated with transportation? | Pages 1-2 and 10-11: interactions among system mass, logistics, spares, propulsion, and objectives |
| What crew size and duration does this study assume? | Page 3: approximately 1,000-day conjunction-class mission with four crew; includes return |
| What categories of supplies does its logistics model include? | Page 3: consumables, spares/maintenance, gases/liquids, and packaging |
| Does more recycling necessarily minimize total mass or cost? | Pages 10-11: preferred options depend on objectives, mission assumptions, and interactions |
| Which limitations should accompany conclusions from this model? | Pages 4 and 11: exploratory scope, fixed habitat sizing, additional modeling deferred |
| Who is the named captain of this mission? | No roster or captain was identified in reviewed sections; candidate insufficient-evidence test, pending a full-document absence check |

Do not assign the full collection an insufficient-evidence label from a sampled review alone. Before scoring the last question, search and inspect the complete test corpus and confirm the intended scope.

## Follow-up work

1. Reconcile unresolved version, publication, reuse, and contributor metadata; keep unknown values explicit.
2. Create page-preserving extraction for the selected document and inspect the output. Inspection scratch text is not a production corpus.
3. Review and finalize a small evaluation set, including answerable, partial-evidence, and insufficient-evidence cases.
4. Add a retrieval baseline; assess returned evidence before selecting a generation provider or building the browser chat.
5. Add sources for uncovered topics only when needed. Captain/crew roles, a daily schedule, micrometeoroid protection, voice interaction, and complete mission sequencing are not established by this review.

## Preservation and tooling

Local SHA-256 values are in the source register. A final read-back check compares all seven originals with their registered hashes. Inspection used a temporary PyMuPDF environment, not an application dependency. No application code, production extraction pipeline, retrieval index, model configuration, or UI was added.
