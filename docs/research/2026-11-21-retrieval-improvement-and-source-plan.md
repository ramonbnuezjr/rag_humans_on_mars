# Retrieval improvements and targeted collection expansion

Date: 2026-11-21 (America/New_York)

Status: implementation and verification record. Any research synthesis here is preliminary and combines multiple mission concepts; their assumptions remain separate. This is not an approved mission design, medical guidance or a validated radiation safety assessment.

## 1. Radiation extraction

Added an optional local spacing parser: pdfplumber 0.11.8 with pdfminer.six 20251107. It uses geometric gaps (`x_tolerance=1`, `y_tolerance=3`, layout disabled), without OCR or guessed word segmentation. Pypdf remains the default parser and supplies label metadata/initial validation. Parser/dependency versions and settings participate in extraction identity. See [parser documentation](https://github.com/jsvine/pdfplumber#extracting-text).

For the 65-page radiation PDF, the count of alphabetic strings at least 25 characters long fell from 561 in the previous pypdf output to zero in the new output. This is a diagnostic heuristic, not a word-accuracy score. Sampled PDF pp. 24, 44 and 46 were checked against rendered originals: model assumptions, active shielding concepts/development limits and material discussion are readable. Previous pypdf plain/layout comparisons had not fixed spacing. All 65 new page records are nonempty and retain source/page metadata. The new index contains 284 passages, compared with 244 previously; recovered spaces change word-based chunk boundaries.

Old output files remain intact, with previous extraction/index pointers in the register's processing history. Tables, figures, equations, superscripts, dose units, rotated front matter and whole-document reading order are not certified by this improvement. The original arXiv version/publication/license and scientific applicability caveats remain.

## 2. More realistic questions

Saved twelve draft agent-reviewed questions covering mission assumptions, dehydrated food, integrated vehicle design, medical evacuation, arrival fitness, active shielding, shield materials, medical AI, a complete mission route, daily life, puncture repair and governance.

The initial [three-source cases](../../evals/research-retrieval-v1-three-source.jsonl) contained eight expected-evidence targets, including partial-support cases, and four manual gaps. Expected support appeared at top five for 6/8 source-scoped questions and 5/8 combined questions. See [source-scoped results](../../evals/results/research-source_scoped-4a601ec9afec3b6c9c54d8d9a3a56d1c1a95e80aea176f4162f489832e9c424a.json) and [combined results](../../evals/results/research-combined-395eaff0a631438a7f06d3fe54430f44ab4e582ec86416e2f549f7b7aaa9a4a6.json).

The expanded [five-source cases](../../evals/research-retrieval.jsonl) retain the questions but add evidence targets and qualifications for architecture and daily operations. Expected source versions are bound to SHA-256. This version contains ten scored evidence-location targets and two manual gaps. Results: 7/10 source-scoped, 4/10 combined at top five. See [source-scoped results](../../evals/results/research-source_scoped-e8d57274bcdd5a12b187e7ed1e0f07854b42ec987ffc177178341b5fe5fb97ab.json) and [combined results](../../evals/results/research-combined-61ddc77dccba730b9eb61cc778a1cf42d200b1f4cda6c9832953a5ac62d47904.json). Different case definitions/corpus sizes mean the two ratios are not directly comparable.

Within the expanded set, source-scoped retrieval misses the selected targets for integrated design, arrival fitness and the complete route. Combined retrieval additionally misses the selected targets for mission assumptions, medical return and daily life. It does retrieve the selected passages for dehydrated meals, active-shield limitations, shield materials and medical AI. Some returned passages may be relevant alternatives to the narrow labels; misses are not proof all results are useless. A complete relevance review has not been performed.

These are development questions, not an independent or held-out benchmark. Partial cases check relevant evidence location, not complete answers. Two gap cases remain unscored: micrometeoroid puncture procedures and legal authority. Incidental matches are displayed but cannot count as successful abstention. No evidence-sufficiency classifier or answer generation exists. Earlier eleven source-specific checks still pass; their easier success did not predict realistic-question performance.

## 3. Combined retrieval

`search all` loads every active registered index, verifies original/extraction/index integrity and builds an in-memory union. It recomputes BM25 document frequencies, average passage length and ranking over that union; per-source BM25 scores are not compared directly. Compatible index settings are required. Any invalid included source fails the operation instead of silently shrinking coverage. Unindexed files are excluded.

Source ID, edition, source hash, extraction/index IDs, exact character offsets, PDF position and reviewed labels remain attached to passages. CLI output shows the source's mission context, evidence type, review status and extraction limitations. Adjacent-page context and concept reconciliation remain manual; no automatic source diversity, synonym expansion, semantic embeddings or reranking was added.

The larger source collection can displace a desired passage with other keyword matches. This is the measured next retrieval problem; adding PDFs is not a ranking fix.

## 4. Targeted additions from observed gaps

Only two PDFs were downloaded, both directly from NASA, with original filenames, URLs, acquisition timestamps and byte hashes recorded in the [register](../../sources/registry.json). Both were extracted and indexed locally. Existing original PDFs were preserved.

- `mars-008`: [Human Exploration of Mars Design Reference Architecture 5.0](https://www.nasa.gov/wp-content/uploads/2015/09/373665main_nasa-sp-2009-566.pdf), NASA/SP-2009-566, July 2009; 100 PDF pages and 397 passages. Title page identifies the Mars Architecture Steering Group and editor Bret G. Drake. This is a historical reference architecture, not a current approved flight plan. The full report was deliberately distinguished from the similarly titled February 2009 NTRS presentation. PDF p. 18 (printed p. 4) outlines crew transit, predeployed assets, ascent and return; other sections cover launch, propulsion and landing. Reuse terms remain unverified. Three blank-text pages (5, 6, 99) were retained, not discarded; no claim of complete visual/OCR coverage is made.
- `mars-009`: [Overview of Crew Operations for Transit to Mars](https://ntrs.nasa.gov/citations/20230012629), Piontek and Luckey, AIAA ASCEND 2023 context; 11 PDF pages and 41 passages. Its SAC21 example uses four travelers, two landing for 30 sols and two remaining in orbit, over an 850-day mission (PDF p. 2). PDF pp. 3–4 discuss crew activity categories and reproduce ISS workday guidance; these are not an approved Mars schedule. PDF p. 8 describes transit and arrival preparation. Exact publication date remains null; catalog acquisition/conference dates were not substituted for publication. NASA catalog permits public use of this US Government work.

These additions improve architecture and operations coverage. They do not establish a particular spacecraft interior, a named captain, an individual roster, a complete Mars timetable, validated permanent settlement, puncture repair procedures or governance. Do not transfer DRA 5.0 crew/vehicle assumptions into SAC21 or the approximately 1,000-day ECLSS study. Full scientific/current applicability review remains pending.

## Preservation and software verification

Five indexed sources now contain 267 PDF pages and 993 passages. Nine original PDFs are registered; four owned PDFs remain unindexed (broad Mars technology report, oxygen-recovery development, Mars-GRAM 2024 and 2021). All nine originals match their registered hashes. All five index/extraction checksums and exact passage slices were checked. Selected new/improved extraction and index reruns reused deterministic outputs; previous radiation outputs remain available.

Eighteen software tests pass on Python 3.11. They cover optional-parser provenance/preservation, valid page/label records, combined corpus-wide ranking and per-hit provenance, exclusion of unindexed sources, failure on stale included indexes, CLI use and unscored gap handling/version checks. A synthetic fixture was corrected to use valid indirect PDF content streams when the second parser exposed malformed direct streams. Python 3.9 syntax passes; remote CI/runtime on 3.9 has not been run here. CI now installs the optional spacing extra.

No embeddings, generation/model service, external document upload, UI, voice, Git publication or PR was enabled. Network use was limited to parser-package installation and source discovery/acquisition. All source PDFs and generated artifacts remain excluded from Git.

Processing manifests:
- `mars-006`: [extraction manifest](../../data/processed/mars-006/dc28a96c2be6c1de707e77c693d75cc8a93cd823e9a804f07152f9e29e069654/89ea88a5a59273e873f777fbd19bd57a452d83cecf8c1f4373df9375da493f10/manifest.json) and [index manifest](../../data/index/mars-006/e80e72829e120cec4798f57b9933863c949df0a1ff9d7bda1f2d368c53cb4703/manifest.json).
- `mars-008`: [extraction manifest](../../data/processed/mars-008/1b3f956984f527c73ef43d4da18a0207c56cfdc38dc2d84a0c158fb65b596833/98909cbf6dca324309cbedfc84da828f57d6cfdf3068183d4a31ee9d905a539d/manifest.json) and [index manifest](../../data/index/mars-008/4d43dc4f18033f25526f3baf8c3843221a5be9e6f843ac958cc411c030b035c2/manifest.json).
- `mars-009`: [extraction manifest](../../data/processed/mars-009/6697bacbccdc266bb24ca21a85f987243221d73215d6ce6fd8faa8ff160b1c35/7f7d07acbd4fb9ce0a2ad18bb5743ea190de021a2f58988811c6de996a4a097f/manifest.json) and [index manifest](../../data/index/mars-009/03a4277278bce91294ee38a9e46c785113f845a403a5a1e67cfdbd7c0a054971/manifest.json).

## Reproduce and interpret

```sh
.venv/bin/python -m pip install -e '.[extraction_spacing]'
.venv/bin/mars-rag search all "Why does recycling water matter when packing food?" --top-k 5
.venv/bin/mars-rag evaluate all
.venv/bin/python -m unittest discover -s tests -v
```

`evaluate all` intentionally exits 1 while selected evidence targets are missed. Software tests pass independently. Extraction with `--parser pdfplumber` writes output but requires review and registration of the extraction pointer before indexing; it does not silently promote a new run.

## Remaining work and follow-up questions

- Review alternate relevant passages and the failed targets before changing ranking or labels. Would source selection, query rewriting, stemming, title matching, source diversity or adjacent-page context address measured failures? Test changes against independently selected questions too.
- What evidence threshold will make retrieval reliable enough for the first generated-answer MVP? No acceptance threshold has yet been agreed.
- Which contemporary medical/radiation primary evidence is needed for the selected questions, and which numerical tables actually need structured verification?
- Which habitability/layout or repair/governance questions justify the next source? Inspect owned material before downloading overlapping documents.
- Provider choice and explicit external data boundaries remain required before hosted embeddings or generated answers. Chat UI and voice follow reliable evidence retrieval.
