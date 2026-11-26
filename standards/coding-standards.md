# Coding standards

Scope: code, tests, settings, dependencies and development workflow. Sources: [SSDF 1.1](reference/README.md#sources) for secure development principles; [PEP 8](https://peps.python.org/pep-0008/) for Python naming/style. Tooling and repository choices below are project policy.

## Implementation and scope

- **CODE-01 [Project; adapted SSDF PW.8]** Add focused tests for meaningful behavior and failure modes. Use `unittest` and synthetic or redistributable fixtures. Keep draft research questions labeled draft; distinguish software correctness, retrieval checks and answer/evidence coverage. No percentage coverage target is imposed.
- **CODE-02 [Project]** Update `status.md` when behavior, decisions or next steps materially change. Update relevant usage/architecture documentation; keep progress history out of `AGENTS.md`. No parallel changelog is required.
- **CODE-03 [Project]** Distinguish implemented, proposed, simulated and unverified behavior in code/docs and summaries. Do not present a mock or placeholder as working functionality, or a retrieved match as a complete supported answer.
- **CODE-05 [Project]** Keep changes small enough to inspect. Require a concrete owner requirement before adding orchestration frameworks, hosted databases, agents or new UI capabilities. Record consequential architecture decisions; obtain missing decisions about dependencies, runtime/tooling changes or external services before enabling them. Existing explicit authorization need not be requested again.
- **CODE-10 [Project; adapted PEP 8]** Put application code in `src/mars_rag/`; use descriptive snake_case names and follow nearby readable conventions. Do not reformat unrelated files. Preserve the relative `CLAUDE.md -> AGENTS.md` link.
- **CODE-21 [Project]** Validate external data's type, bounds and allowed values explicitly at its boundary. Existing stdlib validation is acceptable; Pydantic is not required. Keep SQL parameterized and subprocess inputs separated from shell code under SEC-11/SEC-12.
- **CODE-30 [Project; adapted SSDF PW.4]** Keep the core stdlib-only unless a new dependency is explicitly chosen. Put optional tools/dependencies in the appropriate separate configuration; record exact selected versions and reproducibility implications. Inspect package identity, maintenance, license and available vulnerability information before adding/upgrading it. Report unavailable checks and unresolved findings; do not silently install a proposed package or claim it was scanned.
- **CODE-40 [Project; adapted SSDF PW.5]** Handle an exception where recovery or a safe boundary response is possible. For new broad exception handlers, explain why the boundary requires them. Do not hide failed storage/search behind a success message. CLI output may use `print`; no new logging framework is required.
- **CODE-50 [Project]** Keep model/provider configuration separate from retrieval logic. Apply SEC-23 and IAM-40 before an external provider is enabled; do not introduce an implicit provider or model selection.

## Evidence and reproducibility

- **CODE-60 [Project]** Store provenance in `sources/registry.json`. Do not infer authors, publishers, URLs, dates or licensing from filenames; record unknowns as unknown.
- **CODE-61 [Project]** Preserve source IDs, editions, hashes, extraction/index identities, page references and relevant offsets through processing. Keep generated text/indexes reproducible and outside Git. Keep different source editions and immutable processing outputs separate; source-file preservation is governed by SEC-02.
- **CODE-62 [Project]** Preserve original questions and review provenance when evaluating retrieval. Report regressions and limitations; distinguish known development cases from fresh independent validation. Feedback ratings and BM25 values are not calibrated accuracy/confidence probabilities.
- **CODE-70 [Project]** Preserve unrelated user changes. Do not push, publish, open a pull request or merge without the owner's request. Do not rewrite existing commits or bypass hooks/signing to obtain a green result.

## Current compatibility and tooling

Python `>=3.9` remains the declared compatibility baseline in `pyproject.toml`; this adoption does not change it. Python 3.9 is end-of-life, so compatibility is not an endorsement of it as a maintained deployment runtime. A supported baseline and CI/dependency compatibility require a separate explicit upgrade decision; see the [decision record](../docs/decisions/2026-11-25-project-standards.md).

Black, Ruff, strict mypy, pre-commit suites, pytest and schema libraries are not mandated or installed by these standards. A development-only Ruff evaluation may be proposed separately. No lockfile/scanner is claimed to exist; runtime dependencies, transitive resolution and build tooling need separate treatment when reproducibility controls are expanded.

## Checklist

- [ ] Change serves the authorized outcome; relevant status/docs are updated (CODE-02/03/05).
- [ ] Meaningful tests and failure checks ran, or their omission/blocker is explicit (CODE-01/40).
- [ ] Naming, validation and provenance are preserved (CODE-10/21/60/61).
- [ ] New dependencies, providers and runtime/tooling changes have explicit decisions (CODE-30/50).
- [ ] Results are honestly qualified; unrelated changes and Git publication boundaries are preserved (CODE-62/70).
