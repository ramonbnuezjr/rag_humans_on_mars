# Radiation and medical processing; collection coverage

Date: 2026-11-21 (America/New_York)

Status: processing verification and preliminary collection assessment. Topic coverage combines multiple mission concepts; it does not define one approved mission or establish scientific consensus. Coverage judgments are based on sampled content, not exhaustive review.

## Completed processing

| Source | PDF pages retained | Page-bounded passages | Local processing |
| --- | ---: | ---: | --- |
| `mars-004`, [2017 medical risk report](https://ntrs.nasa.gov/citations/20170004604) | 79 | 217 | Extracted, indexed, sampled prose checked |
| `mars-006`, [radiation modeling paper, arXiv v2](https://arxiv.org/abs/2208.00892v2) | 65 | 244 | Extracted, indexed, sampled prose checked; word-spacing defects remain |
| `mars-007`, [life-support tradeoff paper](https://ntrs.nasa.gov/citations/20205001088) | 12 | 54 | Previously extracted/indexed; integrity and retrieval checks rerun |
| **Total searchable** | **156** | **515** | **Three source-specific indexes** |

No PDFs were downloaded, overwritten, or merged. All seven local PDF SHA-256 hashes still match the [register](../../sources/registry.json). Processing used the existing application without code changes, embeddings, model calls, or external document transfer. The relative symlink remains `CLAUDE.md` → `AGENTS.md`.

For both new sources, extraction retained one sequential, nonempty record per PDF page. Original hashes, extraction/index checksums, and all new passage offsets were verified. Every indexed passage equals its exact slice of the extracted page. Identical extraction/index reruns reused the same output. Nonempty text does not establish complete or correct extraction.

Only visually checked printed labels were recorded: medical PDF positions 11 and 32; radiation positions 24 and 44. Other printed labels remain null. Every page retains its one-based PDF position. Neither new PDF has embedded PageLabels.

Generated files:

- Medical [extraction](../../data/processed/mars-004/71260e17660a4cdbd6232b739edc650aa4dd6164fee362c7196dff44b34168e2/d084a3b4a6ab37f8f7dfaf2284f313ab1c5608c66eb8ba5d32c537b012089a70/manifest.json) and [index](../../data/index/mars-004/2a33fce1bfc4708f1cff0c6ea5d0367f9da60fa31967c0c5b4d18a9594a41257/manifest.json).
- Radiation [extraction](../../data/processed/mars-006/dc28a96c2be6c1de707e77c693d75cc8a93cd823e9a804f07152f9e29e069654/72e8cb3555d9f2f707e9e6109547bc5229b270cd4ad2b7c42eac171af1f289b4/manifest.json) and [index](../../data/index/mars-006/cd8d9698073a6b64c536fc91151286ded78277c1474ec4440ace1303735bedea/manifest.json).

Outputs remain excluded from Git. Review caveats are attached to the source extraction records in the register; the CLI does not yet display those extra caveats on every search result.

## Evidence boundaries

The [medical report](../../data/raw/20170004604.pdf), PDF p. 11, supports the need for onboard medical autonomy under communication and evacuation constraints. PDF p. 32 describes decision support and onboard knowledge resources, distinguishing existing ISS/terrestrial examples from capabilities still needing development. This is a 2017 evidence report, not current medical policy or a demonstrated Mars medical system. Its cited quantitative communication assumptions and historical training requirements need contemporary verification. The unresolved release-date placeholder and contributor/catalog differences remain documented in the register.

The [radiation paper](../../data/raw/2208.00892v2.pdf), PDF p. 24, uses GEANT4 and a modified MIRD human phantom, compares unshielded exposure with 5 g/cm² aluminum shielding, models solar conditions, and omits minor heavier cosmic-ray species. These are model assumptions, not astronaut measurements on a Mars mission. PDF p. 44 describes electrostatic/plasma/magnetic shielding concepts and development limitations; cited simulation results are not operational protection guarantees. The local document is arXiv v2 dated 5 January 2023; journal publication, peer-review status, license, and current applicability remain unverified.

Radiation extraction joins some words, notably on PDF p. 44 and also elsewhere. A sampled comparison of pypdf plain/layout modes did not fix this. Raw extracted text was preserved without guessed word reconstruction. This can impair keyword recall and readability. Tables, equations, plots, dose units, numerical relationships, referenced studies, and whole-document reading order have not been validated. Prose retrieval passing does not clear these defects. Before numerical dose answers or broad radiation use, improve extraction and validate representative hard passages against rendered originals.

## Provisional retrieval checks

Cases were selected from inspected prose; they are agent-reviewed development checks, not a held-out benchmark, human approval, completeness grading, or generated-answer evaluation. Expected pages and phrases were not changed after the first scored run. All five new cases passed at top five; three found expected support first.

| Question focus | Expected PDF page | Supporting passage rank |
| --- | ---: | ---: |
| Medical autonomy under communication/evacuation constraints | 11 | 1 |
| Onboard medical decision support | 32 | 1 |
| GEANT4/MIRD body model | 24 | 2 |
| Radiation model shielding assumptions | 24 | 1 |
| Active shielding readiness limitations | 44 | 2 |

The shielding case checks one supporting phrase, not every assumption asked about. Rankings can also include contents pages, references, or incomplete context. Search scores do not indicate evidential confidence.

- Medical [cases](../../evals/mars-004-retrieval.jsonl) and [results](../../evals/results/mars-004-c568c39091718feaa95bccb088f98ec7ad8696791010fd52902063bbb6038e23.json).
- Radiation [cases](../../evals/mars-006-retrieval.jsonl) and [results](../../evals/results/mars-006-fb67a207dfdbfc190c472598c89075a718538f36e9623e452d11d017f0c5668e.json).
- Existing life-support checks still pass: five evidence cases at top five plus one lexical no-match probe. The probe does not establish reliable insufficient-evidence handling.

## Inventory: already owned versus still needed

Seven PDFs represent six distinct titles; two are separate Mars-GRAM editions. The original three now have content/catalog identity checks recorded; full source review remains pending for all seven.

| Already owned, not yet indexed | Scope and limitation |
| --- | --- |
| `mars-001`: [Approaches To Humans-Mars Both Safe and Affordable](https://ntrs.nasa.gov/citations/20220007320), NASA/TM-20220007320, July 2022 | Broad technology and mission/settlement discussion, including robots, ISRU, power, and shielding. Many ideas are proposals. Sampled PDF pp. 5–14 do not establish a validated integrated mission. |
| `mars-005`: [oxygen-recovery development paper](https://ntrs.nasa.gov/citations/20200003267) | Laboratory development of oxygen recovery; not an operational Mars system or complete food/water/power design. |
| `mars-002`: [Mars-GRAM 2024 guide](https://ntrs.nasa.gov/citations/20240012934) | Engineering atmospheric model; useful to atmospheric/entry studies, less immediate for crew transit questions. |
| `mars-003`: [Mars-GRAM 2021 guide](https://ntrs.nasa.gov/citations/20210023957) | Distinct earlier edition. Preserve separately; detailed differences have not been reviewed. |

NASA catalog dates for these original three are recorded as catalog dates, not inferred from filenames or treated as actual acquisition dates. Catalog matching does not establish byte identity with a remotely hosted PDF.

## Coverage against the ten research anchors

| Anchor | Current partial evidence | Remaining dedicated evidence need |
| --- | --- | --- |
| 1. Mission architecture and return/permanent stay | Life-support paper has a notional four-person, approximately 1,000-day conjunction-class mission including return; broad options in `mars-001` | An explicit end-to-end reference architecture covering launch, assembly, propulsion, transit, landing, prepositioning, ascent and return. Permanent stay requires a separate concept. |
| 2. Crew/vehicle size and fleet choice | Life-support mass/logistics tradeoffs; medical accommodation constraints | Habitable volume, redundancy and fleet/rescue trade studies; four crew is an assumption, not an optimum proved by this collection. |
| 3. Radiation | Modeling/review paper now searchable | Better text extraction, numeric verification, primary measurements, and current protection standards/uncertainties. |
| 4. Health and gravity | Medical risk and autonomy review | Dedicated reduced/partial-gravity, exercise, behavioral health and artificial-gravity evidence; sustained Mars-gravity outcomes remain unresolved here. |
| 5. Air/water/food/power | Life-support tradeoffs indexed; oxygen development owned | Integrated power/thermal, long-duration food storage and nutrition, agriculture and surface life-support evidence. |
| 6. Roles and daily life | Medical role/training discussion | Crew operations, habitability, schedules, command, cross-training and workload. |
| 7. Damage and repair | Spares/logistics tradeoffs, broad technology proposals | Micrometeoroid protection, leak detection, containment, maintenance, repair limits and emergency procedures. Radiation shielding does not establish impact protection. |
| 8. Sustainable outpost | Broad ISRU/robotics proposals in `mars-001` | Validated resource/process data, dependency inventories, resupply failure cases, power, manufacturing and agriculture constraints. |
| 9. Funding and governance | No dedicated source identified in sampled collection | Funding/operating models, law, authority and governance. |
| 10. AI/robots and human control | Medical decision-support discussion; broad autonomous-robot proposals | Mission-specific autonomy, human authority, verification, failure recovery and demonstrated capability boundaries. |

These are identified coverage gaps, not proof that no incidental mention exists in any unsampled page. A focused MVP need not answer all ten anchors.

## Recommended next steps

1. Agree on a small MVP question set around mission assumptions, life support, radiation and medical autonomy. Independently review expected evidence; add paraphrases, partial support, contradictory concepts and insufficient-evidence cases. Improve radiation extraction where these cases expose failures.
2. Add combined retrieval across the three indexes; search currently requires a single source ID. Preserve concept/version attribution and adjacent-page qualifications. This is proposed work, not implemented here.
3. For broader journey coverage, prioritize a detailed reference mission architecture and a crew operations/habitability source. Inspect `mars-001` and `mars-005` before acquiring overlapping papers. Defer bulk acquisition and Mars-GRAM indexing unless selected questions need them.
4. Choose generation/provider and document external content transfer before adding answers. Then evaluate citation support and appropriate insufficient-evidence responses. Chat UI and voice follow a reliable text/evidence path.

## Follow-up questions

- Which mission concept and time horizon should define the first answer set?
- Can a parser/configuration change recover radiation word spacing without guessed text or losing provenance?
- Which numerical radiation results are actually needed, and what assumptions/units must accompany them?
- Which medical conclusions have changed since the 2017 review?
- Which two or three unanswered MVP questions justify acquiring the next sources?

No additional acquisition, application changes, generation service, web interface or voice setup was performed in this step.
