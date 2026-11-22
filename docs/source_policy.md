# Source collection policy

## Before adding material

Prefer original reports and papers over summaries. Collect against a research question instead of maximizing file count. Public access does not automatically establish permission to redistribute a document.

Potential collection areas: mission design and transport; entry, descent and landing; atmosphere and weather; radiation; habitats and life support; water and food; energy; medicine and human factors; maintenance and long-term resilience.

Use question-level evidence gaps to guide future acquisition: record what current evidence supports, what is unanswered and which mission concept applies. Check whether extraction or ranking missed existing support before treating a gap as missing documents. Proposed coverage labels and a research-gap register are not implemented. Owner feedback should distinguish partial support from a complete answer; adding a document alone does not close a gap. No automatic downloads or crawling are enabled.

## Register every source

Add a stable ID and local path to `sources/registry.json`. Record the content hash, canonical URL, title, authors, publisher, publication date, edition, acquisition date, document type, topics, reuse terms, and metadata review status. Use `null` for unknown facts. Keep filenames unchanged until identity and edition are verified.

Classify evidence during review: measured observation, experiment, simulation, engineering proposal, review article, or commercial claim. Institutional origin alone does not settle the strength or applicability of a claim.

## Initial collection

The three original PDFs were initially registered by filename and SHA-256 only. Subsequent sampled content/catalog checks established their identities; full scientific and reuse review remains pending. Filenames alone never establish provenance. The two Mars-GRAM guides are distinct 2024/2021 editions and must remain separate. See [current status](../status.md) for the expanded collection and active indexes.

## Updates and duplicates

Use SHA-256 to identify byte-identical duplicates. Check publication dates and revisions for similar documents. Retain superseded versions when needed to explain differences, recording which edition supersedes which. Do not silently overwrite originals or automatically resolve conflicting findings.

## GitHub boundary

Commit the register, code, documentation, and small reviewed evaluation fixtures. Keep PDFs, extracted text, indexes, credentials, and generated answers out of Git by default. Check reuse permissions before sharing document excerpts or adding downloadable sources. Before public release, review the staged files and source metadata for anything you do not intend to publish.
