# Ranking review, demonstration and default decision

Date: 2026-11-21 (America/New_York)

Scope: review existing evidence and improve retrieval only. No new documents, generated answers, embeddings, provider service or web/voice interface were added. The nine originals and five immutable indexes are unchanged.

## What the missed results showed

The [unchanged development targets](../../evals/research-retrieval.jsonl) identified six combined-search misses:

| Question | Review of original result and missed evidence | Outcome with experimental reranking |
| --- | --- | --- |
| Mission assumptions | Top result: DRA launch processing, PDF p. 44. Selected ECLSS assumptions: PDF p. 3, originally supporting chunk rank 28. Everyday wording and source terminology differ. | Selected page/chunk now first. |
| Integrated design | A drilling-equipment failure passage outranked the selected ECLSS integrated power/propulsion discussion on PDF p. 10; selected chunk below top 100. | Still misses selected p. 10. It selects other ECLSS pages, which need relevance review. |
| Medical return | Ascent/transport text ranked above medical evacuation constraints on PDF p. 11; selected support rank 10. | Selected support now second. |
| Arrival fitness | Radiation and broad crew-health mentions outranked medical deconditioning/rehabilitation on PDF p. 29; selected chunk below top 100. | Selected support now second. |
| Complete route | Top DRA p. 41 is relevant architecture evidence, despite missing the selected ascent/return support on p. 18 (supporting chunk rank 55). Thus the narrow miss is not wholly irrelevant retrieval. | Selected page now third; selected phrase is in its full-page context, not its anchor chunk. |
| Ordinary day | Medical exercise discussion ranked first; crew-operations PDF p. 3 was just outside top five. | Selected page/chunk now first. |

No expected source/page/phrase labels were changed to obtain these gains. The governance case still has a historical three-source phrase in its answer-boundary annotation; its current label remains an unscored sampled-coverage judgment, not proof the full collection lacks all legal material. Human label review remains needed.

## Implemented methods

- `--ranking baseline`: unchanged original chunk-level BM25 ranking and short anchor excerpts.
- `--ranking page` (**default**): exactly the same ranked chunks/scores, plus the complete verified extracted PDF page. This improves access to context while preserving ranking behavior.
- `--ranking context` (**experimental**): lower-weight query hints from a small explicit glossary, combined chunk/page BM25 scores, limited subject-word title boosts, and one result per source/page. Original chunks remain unchanged; complete page context is also returned. Configuration is visible in [ranking.py](../../src/mars_rag/ranking.py).

The glossary connects examples such as weightlessness/microgravity, life support/ECLSS and ordinary day/workday. It is development-informed, limited and potentially wrong in other contexts. It contains no case IDs, source IDs, expected pages or answer text. No semantic model or medical reasoning is implemented.

Both context modes preserve the anchor chunk ID/text/offsets and add separate exact full-page text, context ID and full-page offsets. The CLI explicitly identifies the displayed text as a complete extracted PDF page and shows query hints for the experimental method. Adjacent pages, table structure and scientific sufficiency are still not inferred.

## Matched comparisons

Corpus: the same five sources, 267 pages, 993 chunks. Fixed `top_k=5`. Reports record index/source identities, dataset hash, ranking version/configuration hash, returned source/page/chunk/context IDs, and separate anchor versus page-context hits.

Eight [additional validation questions](../../evals/ranking-validation.jsonl) were frozen before candidate experiments. Candidate comparisons were made on development questions, then checked against this separate set. Both sets are agent-authored; this is not independent human evaluation or a blind held-out benchmark. The validation results have now informed the default decision and cannot be treated as untouched future tests.

| Method | Development evidence targets found | Separate validation targets found | Evidence unit |
| --- | ---: | ---: | --- |
| Original baseline | 4/10 | 7/8 | Short anchor chunk |
| Original ranking + page context | 4/10 | 8/8 | Complete returned page |
| Experimental reranking + page context | 9/10 | 7/8 | Complete returned page |

Experimental anchor-only hits are 7/10 development and 6/8 validation. Thus the headline 9/10 includes two cases where surrounding same-page text supplies the expected phrase; it is not 9/10 improved short excerpts. Its development top-one page-context hits are 4/10, compared with the baseline's 1/10 anchor hits. Two existing development gap questions remain unscored for every method. These are expected-evidence location checks, not complete relevance, answer accuracy, abstention or scientific-validity scores.

The separate departure-preparation question benefits from full-page context: its baseline already selected the right page but the selected short chunk omitted the expected fuel-check phrase. Experimental reranking loses the maintenance-delay target on crew-operations PDF p. 5, which the original ranking returned fifth. That regression prevents claiming that experimental ranking generalizes better.

### Saved comparisons

- Development: [baseline](../../evals/results/research-combined-9c1fdbca0b4895a9db8849c5fc5e1adc59a6755f64f86b2b68de8629802dae53.json), [page default](../../evals/results/research-combined-fcdffc5c9b2738002c50dcedeb52f172d19c64acc20e3867527f5e8d948616e2.json), [experimental](../../evals/results/research-combined-f39c0d04da677d36db0091f946d87a183fcdbeb6282bb6894c8eacb923300e09.json).
- Validation: [baseline](../../evals/results/research-combined-496d3944241709581f99acacf2e1656459156aadbedc979b792953f43d4adfc8.json), [page default](../../evals/results/research-combined-e5050d2c1bc447e50f97931741c42442186bcc23387b74ece686de12a25f338b.json), [experimental](../../evals/results/research-combined-70e24862cb44993c478918b1036618de8cce73ea0ee18617130169321fbd93f4.json).
- Experimental source-scoped development: [9/10 page-context, 7/10 anchor](../../evals/results/research-source_scoped-0ce881a94c17d86a76068eedc8406a74fb704dd3bed2c051f1b899e6fd6bb068.json).

## Demonstration

Question: “Is the thousand-day figure the trip to Mars, and how many people does the life-support study assume?”

Original first result: `mars-008`, DRA 5.0, PDF p. 44, discussing spacecraft launch-processing facilities. Experimental first result: `mars-007`, ECLSS tradeoffs, PDF p. 3, containing the approximately 1,000-day conjunction-class/four-crew assumption. The experiment retrieves evidence; the application does not generate an explanatory answer or establish outbound transit duration from this excerpt alone.

```sh
.venv/bin/mars-rag search all "Is the thousand-day figure the trip to Mars, and how many people does the life-support study assume?" --ranking baseline --top-k 1
.venv/bin/mars-rag search all "Is the thousand-day figure the trip to Mars, and how many people does the life-support study assume?" --ranking context --top-k 1
.venv/bin/mars-rag evaluate all --ranking context
.venv/bin/mars-rag evaluate all --eval-set ranking-validation.jsonl
```

The experimental development evaluation exits 1 because one expected target remains missed. The default validation evaluation passes 8/8. The default development evaluation still exits 1 at 4/10. Software correctness and evidence-location coverage remain separate.

## Verification and decision

Twenty-two software tests pass on Python 3.11, including exact parent/anchor offsets and IDs, unchanged baseline order/scores, page diversity, phrase-bounded query hints, separate anchor/context evaluation, dataset path boundaries and stale-source failures. The earlier eleven source-specific checks still pass under the new page default. All nine original hashes and five index checksums remain valid; Python 3.9 syntax checks pass. Remote CI/3.9 runtime were not executed here. Temporary experiment files were removed.

Keep `page` as the default because it supplies useful context without a demonstrated ranking regression. Keep `context` opt-in as a concrete development improvement whose generalization remains uncertain. Neither method determines whether evidence is sufficient to answer.

## Owner review and smallest useful next step

Review the mission-assumption demonstration and the maintenance-delay regression side by side. Confirm whether the selected passages actually support the intended question, whether another returned passage should count as relevant, and whether a full page is useful or too much context.

Next, review three concrete cases: integrated design (remaining development miss), maintenance delay (validation regression), and one successful result. Record acceptable supporting passages and necessary qualifications before another algorithm change. For further tuning, author a fresh separate set; do not repeatedly tune against these validation results and continue calling them held-out.

Generated answers, automatic sufficiency/abstention, semantic retrieval, UI/voice and additional collection remain planned, not implemented in this step.
