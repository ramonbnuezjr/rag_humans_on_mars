# Decision: scoped project standards

Date: 2026-11-25. Status: adopted after owner discussion. This records repository policy, not a completed security audit or certification.

## Context and authorization

The owner supplied a generic standards template and [discussion handoff](reference/2026-11-25-CODEX_HANDOFF.md), initially requiring discussion before any change. The owner then agreed to a practical existing-project baseline, unchanged tooling/focused tests, canonical rule organization, scoped IAM requirements, explicit conflict resolution, checkpoint-before-branch workflow and template retirement after safeguard review. The original proposals remain archived as historical input; they are not active instructions.

Existing feedback/UI/diagnostic work and supplied template drafts were preserved in local checkpoint commit `f708e22` on `main`. Adoption is isolated on `feature/project-standards`, based on that checkpoint. No push, pull request or merge is authorized by this adoption.

## Decisions against handoff section 5

| Question | Agreed resolution |
| --- | --- |
| 1. Existing coding baseline | Adopt standards suited to stdlib, unittest and the current project. Runtime/tooling upgrades are separate decisions; do not use adoption to refactor the app. |
| 2. Black/Ruff/mypy | No new tools now. A dev-only Ruff evaluation may be proposed separately; no formatter/linter/type-checker installation, pin or migration occurs in this change. |
| 3. Coverage | Focused behavior/failure tests. No arbitrary 90% target. Software checks and evidence/retrieval evaluation remain distinct. |
| 4. Rule location | Keep AGENTS.md short: purpose, commands and links. Detailed rules have one authoritative home under standards/. Preserve the CLAUDE.md relative symlink. |
| 5. Security rules | Move existing detailed safeguards intact into canonical coding/security rules, adding scoped local-serving and provider/privacy boundaries. Treat source/model/tool text as untrusted data. |
| 6. IAM now | Keep a short IAM file covering current signing-key/access safeguards and clearly conditional provider/account/remote-access requirements. Do not introduce sign-in, roles or sessions. |
| 7. Provider key details | Defer actual storage/provider configuration until provider selection. Before enabling it, decide environment injection versus keychain/secrets manager, owner, permissions, expiry where supported, revocation/replacement and sanitized audit events. No secret is solicited or installed now. |
| 8. Remote access | Separate explicit exposure/security decision, including authentication through an identity provider/maintained library, HTTPS, server-side route/object authorization, session protections, assurance and safe auditing. Local loopback/Origin checks and review signatures are not authentication. |
| 9. Git workflow | Save existing work as its own checkpoint, then adopt standards on a dedicated feature branch. Preserve all unrelated files and local private data. No publication or history rewrite. |
| 10. Template retirement | Review migrated safeguards and preserve original handoff/decisions before removing standards-template/. The checkpoint retains the complete generic drafts in Git history; they must not remain a second active rule source. |

Conflicts are resolved by applicability, governing instructions and explicit owner decisions, not by a blanket “stricter wins” rule. Material unresolved conflicts are explained before dependent work. Authorized exceptions record scope, reason, risk, validation and follow-up; routine choices already authorized do not require repeated confirmation.

## Original project safeguards: migration review

The pre-adoption AGENTS.md is recoverable from checkpoint `f708e22`. This table maps every former detailed convention/boundary; none was intentionally dropped.

| Former safeguard | Canonical home |
| --- | --- |
| Application code location and descriptive snake_case | CODE-10 |
| Preserve raw originals; never overwrite or silently merge editions | SEC-02 |
| Registry provenance; do not infer author/publisher/URL/date/license from filename | CODE-60 |
| Generated text/indexes reproducible and excluded from Git | CODE-61 |
| No secrets or PDFs in Git; empty settings placeholders | SEC-02 / SEC-20 |
| Separate model/provider configuration from retrieval | CODE-50 |
| Local storage does not establish local processing | SEC-23 |
| Document outgoing content and obtain owner provider choice before external embedding/generation | SEC-23 / IAM-40 |
| Preserve source IDs, versions and page references through processing | CODE-61 |
| Source document text is untrusted data, never executable instructions | SEC-01 |
| No frameworks, hosted databases, agents or UI without a concrete requirement | CODE-05 |
| Focused tests; unreviewed evaluation questions remain draft | CODE-01 / CODE-62 |
| Update material behavior/decisions/next steps in status; no instruction-file progress history | CODE-02 |
| No push/publication/PR without request | CODE-70 |

The entry point preserves reading README/status first and adds the standards index. Its obsolete scaffold-only stage text is replaced by a direction to use current status. Test commands now reference the existing suite/environment. The declared Python baseline itself was not changed.

## Template adaptations and source boundaries

- Generic tooling, Pydantic-at-every-boundary, strict typing/docstring boilerplate, a mandatory changelog and blanket log-framework requirements are not adopted. Existing stdlib validation, CLI output and project documentation remain supported.
- Stable CODE/SEC/IAM IDs begin with this adoption; generic template numbering was not an adopted contract. Future rule changes retire IDs instead of repurposing them. The original generic drafts remain in checkpoint history, not as a competing active policy.
- NIST/OWASP citations identify principles and applicability, not external mandates for our chosen tools. The [reference index](../../standards/reference/README.md) links selected sources; no full standards PDFs or text dumps are downloaded.
- SSDF 1.1 remains the selected final baseline. The referenced 1.2 draft does not silently replace it. SP 800-218A is model-development-focused, not automatically mandatory merely because a coding assistant was used.
- IAM now explicitly acknowledges the existing local HMAC signing key and review receipts. Signature integrity is not authenticated user identity; key ownership/access/lifecycle need deliberate review when changed.
- Python 3.9 is end-of-life. Preserving its current compatibility declaration is not an endorsement of it as a maintained deployment runtime. Selecting/upgrading a supported baseline and CI/dependencies is separate follow-up work, not completed here.

## Verification and limits

Before checkpointing, all 34 software tests passed, as did Python compilation and JavaScript syntax. Adoption validation passed: all 13 former boundary bullets mapped, 36 unique active rule definitions, valid local links, scoped checklists, rule-file length limits and the relative symlink. Each of the nine retired template files was byte-compared against its checkpoint copy before removal; the archived handoff body matches the original exactly. Application, tests, source registry, evaluation definitions, dependency configuration and CI are unchanged against the checkpoint. Do not infer a security audit or dependency scan from these checks.

Known deferred work: supported runtime decision; optional Ruff evaluation; exact ASVS control selection for any future authentication; provider credential design; focused key-storage/access/lifecycle assessment; any improvements from the retrieval diagnosis. No new application protections, automatic restart service, credentials, scanners, hooks, dependencies or confidence features are implemented by these documents.
