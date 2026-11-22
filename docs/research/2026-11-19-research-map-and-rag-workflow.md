# Research map and RAG development workflow

Date: 2026-11-19 (America/New_York)

Status: **Preliminary synthesis combining multiple mission concepts.** The Mars research map spans concepts that must remain separately attributed. The development workflow below is a proposal for this project, informed by public OpenAI guidance; it is not a claim about OpenAI's internal research procedures or an implemented application.

The proposed approach is to map the broad subject, research one bounded question, and alternate further research with small, evaluated software experiments. Completing the entire Mars research program is not a prerequisite for a first retrieval prototype.

## Research anchors

These questions define the proposed map. They are research prompts, not verified findings or completed application capabilities.

1. What happens from launch through arrival? What determines the route and travel time?
2. What spaces, equipment, propulsion, and protection does the crew need?
3. How many people travel? Which skills are needed, and how are responsibilities shared?
4. What do they eat? How do they sleep, exercise, wash, and spend free time?
5. How are radiation exposure, illness, injury, and changes from reduced gravity managed?
6. What maintenance, experiments, training, navigation, and arrival preparations happen during transit?
7. What food, water, medicine, tools, spare parts, and other cargo travel with them?
8. What could fail? What can the crew repair? What happens if continuing or returning becomes difficult?
9. What condition must the crew and equipment be in when they reach Mars?
10. What does an ordinary day aboard the spacecraft look like?

Work primarily on one anchor at a time while recording connections to the others. Each anchor should track its scope, smaller questions, sources and supporting pages, findings, assumptions, disagreements, unknowns, and whether it belongs in the current MVP or later work.

The map can grow. A newly discovered question can be recorded for later without immediately initiating another search. Give each research session a bounded objective and a stopping point.

## First proposed research scope

Start with route and travel time within one clearly identified mission concept. Investigate:

- Which concept, document version, and departure opportunity are being examined?
- What propulsion and trajectory assumptions determine the journey?
- Does the crew enter Mars orbit or descend directly?
- How do duration, propellant, cargo, and crew exposure interact within that concept?

These are open questions. Do not combine duration, crew size, vehicles, and landing methods from different architectures into a single implied mission. The [earlier journey overview](2026-11-19-earth-to-mars-overview.md) remains preliminary, with original-source verification pending; its [follow-up questions](2026-11-19-earth-to-mars-follow-up-questions.md) remain separate.

## Where material belongs

| Material | Location | Purpose |
| --- | --- | --- |
| Acquired original documents | [data/raw/](../../data/raw/) | Preserve source files and separate editions |
| Source metadata | [sources/registry.json](../../sources/registry.json) | Record identity, URL, edition, hash, provenance, and review status |
| Research map, notes, syntheses, and follow-ups | [docs/research/](./) | Record understanding, attribution, and unresolved questions |
| Extracted text and chunks | [data/processed/](../../data/processed/) | Reproducible outputs retaining source and page references |
| Search index | [data/index/](../../data/index/) | Reproducible retrieval data |
| Evaluation questions | [evals/questions.jsonl](../../evals/questions.jsonl) | Check performance against reviewed evidence; existing questions remain draft |

One document may support several anchors. Connect it through references rather than duplicating the original under several topic folders.

Keep original evidence distinct from research notes. An AI-written summary is not independent confirmation of the documents it summarizes. For the first prototype, the proposed evidence index should contain reviewed original-source material, with preliminary syntheses kept outside it.

## Proposed research and build cycle

A practical initial scope is one anchor, one mission concept, one to three relevant documents, and roughly five to ten test questions. These numbers are project suggestions, not OpenAI requirements or a sufficient production benchmark.

1. Research a narrow question manually and inspect the original documents.
2. Record the expected supporting passages and pages for test questions. Include questions the collection cannot answer.
3. Implement extraction for one document and manually inspect prose, tables, units, and page references.
4. Build a simple retrieval baseline that returns passages with source IDs and pages.
5. Compare retrieved passages with the expected evidence and check that the mission concept matches.
6. Later, select a generation provider and document any external content transfer before enabling it. Add answers and check their support and citations.
7. Expand sources or change the software according to observed failures, then repeat evaluation.

The initial research stopping condition is having enough reviewed evidence to judge a small software experiment. A comprehensive Mars library is not required first. This proposal follows the existing [architecture and first working slice](../architecture.md).

## Public OpenAI guidance and project interpretation

[OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) recommends early, task-specific, ongoing evaluation. Its document-Q&A example links the objective, dataset, and metrics. For this project, that supports developing reviewed test questions alongside source research.

[OpenAI accuracy guidance](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) describes an iterative cycle of evaluation, a hypothesis about the failure, an intervention, and reassessment. The proposed application here is to diagnose the failing stage before deciding whether more documents or different code are needed.

| Check | Likely area to investigate |
| --- | --- |
| Is the required evidence present in the collection? | Scope, source review, or acquisition |
| Is the evidence extracted correctly and returned by search? | Extraction, chunking, indexing, or retrieval |
| Does the generated answer accurately reflect the retrieved evidence? | Instructions, generation, citation support, and uncertainty handling |

These checks can reveal more than one failure at once. They are a diagnostic framework, not proof that a single cause has been isolated.

The public documentation supports the evaluation approach; the specific folder conventions, initial scope, and research sequence are proposals tailored to this project. This note does not establish a universal best practice or describe every OpenAI researcher's workflow.

## Deferred actions and follow-up

The owner plans to read the two OpenAI guidance pages before continuing. This is a learning intention, not a completed review.

Later discussion should decide the first mission concept, research boundary, initial documents, expected evidence, and criteria for evaluating the first retrieval experiment. Collection completeness, retrieval quality, and answer support should be assessed separately. No acquisition, implementation, provider selection, or final research-map adoption is performed by saving this note.
