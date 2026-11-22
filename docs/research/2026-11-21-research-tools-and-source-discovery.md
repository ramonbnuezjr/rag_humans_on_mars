# Research tools and source discovery for the Mars project

Date: 2026-11-21 (America/New_York)

Status: **Preliminary synthesis combining multiple mission concepts.** This note concerns how to discover and study evidence for the Mars research map; it does not select or validate a mission architecture. Tool evidence, project recommendations, and unresolved questions are distinguished below.

AI research tools can help find relevant documents and explain selected material. NASA and ESA remain sources of evidence; a research assistant helps navigate and interrogate that evidence. Manually browsing agency websites is not the only discovery method.

## Public evidence about researcher tool use

### Anthropic internal use

An Anthropic study surveyed 132 engineers and researchers and examined internal Claude Code usage. It reports use for debugging, understanding code, implementing features, and data analysis. This documents actual internal use, primarily for technical work; it does not establish a standard toolkit for scientific literature discovery. The study reflects work observed in 2025, rather than a complete current inventory of employee tools. [Anthropic internal study](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)

### Academic scientists using ChatGPT

OpenAI's published study describes academic scientists using ChatGPT for literature review, evidence analysis, coding, and developing ideas. Its participants were academic researchers, not an inventory of OpenAI employees. It therefore does not establish which tools OpenAI researchers use internally. [OpenAI study](https://openai.com/index/science-at-the-frontier/)

### What remains unknown

The discussion did not establish that OpenAI or Anthropic standardizes on NotebookLM or Perplexity. A company's product capabilities, published demonstrations, and employee tool adoption are different kinds of evidence. No comparative benchmark of the tools was conducted, and no tool was selected for the project.

## Match the tool to the activity

| Activity | Required support |
| --- | --- |
| Discover relevant research | Search beyond the current collection and return original-source links |
| Understand selected documents | Explain and compare material with citations into the selected sources |
| Verify a finding | Inspect the original passage, assumptions, date, and mission concept |
| Preserve the work | Retain originals, source metadata, reviewed notes, and open questions |

One product can serve several activities. Begin with one available research assistant rather than assuming several subscriptions are necessary.

## Google notebook tool

NotebookLM, referred to as Gemini Notebook in the Google help page consulted, is a candidate for learning from a small source collection. Google's guidance describes selecting the sources used in an answer and following citations back to supporting passages. Google also documents source discovery from the web. [Source selection and citations](https://support.google.com/gemininotebook/answer/16179559), [source discovery](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-discover-sources/)

These are documented product capabilities, not an independent accuracy evaluation. Citations make answers easier to check; they do not automatically establish that an answer represents its source correctly. Tool availability and behavior can change.

## Proposed workflow

1. Use one research assistant to find candidate documents against a bounded question.
2. Select two or three original documents after checking their abstracts, dates, relevance, and mission assumptions. This is a suggested starting size, not a universal requirement.
3. Explore selected sources in a document assistant, asking for explanations, comparisons, and supporting passages.
4. Verify important passages manually. Record what is supported, proposed, conflicting, or unknown, with mission-concept attribution.
5. Preserve originals in [data/raw/](../../data/raw/), provenance in [the source register](../../sources/registry.json), and reviewed notes in [docs/research/](./). Later, use the reviewed evidence to evaluate the project's retrieval system.

Do not combine values or designs from different mission concepts into one implied spacecraft or itinerary. Preliminary summaries are not independent confirmation of their underlying sources and should remain outside the initial evidence index, as proposed in the [research-map and RAG workflow note](2026-11-19-research-map-and-rag-workflow.md).

## Reusable discovery prompt

> Find up to five original technical documents about crewed Earth-to-Mars transit and life aboard the spacecraft. Prioritize mission architecture and crew operations. For each, provide the original link, date, document type, relevant topics, and mission concept. Distinguish engineering proposals from demonstrated capabilities. Recommend two starting documents and explain why.

## Reusable source exploration prompt

> Using only these sources, explain the journey from Earth departure to Mars arrival. Attribute each detail to its mission concept. Cite supporting passages and identify questions these documents cannot answer.

These prompts are proposals, not completed searches or evidence reviews.

## Follow-up questions

- Which available tool best supports the owner's learning style and access needs?
- Which two or three documents should form the first reviewed collection?
- What claims can be verified directly, and which mission assumptions conflict?
- How will useful findings and citations be transferred into the project without treating generated summaries as original evidence?

Saving this note does not authorize source uploads, acquisition, external-service configuration, or application implementation. No additional PDFs were downloaded and no application code was changed for this documentation step.
