# Standards Index

Agents: read the files below that apply to your task before you start.

| File | Read it when the task... | Rule prefix |
|---|---|---|
| `coding-standards.md` | changes any code | `CODE-` |
| `security-standards.md` | changes any code, config, or dependency | `SEC-` |
| `iam-standards.md` | touches sign-in, tokens, credentials, roles, or permissions | `IAM-` |
| `reference/` | **do not read by default** — only to look up the exact source wording behind a rule | — |

## Two layers, on purpose

1. **Rules (this folder).** Short, imperative, checkable. Each has a stable ID
   and cites the source it came from. This is what the agent works from.
2. **Sources (`reference/`).** The full NIST and OWASP documents, kept so any
   rule can be traced back and so a human or agent can look something up when a
   rule is unclear. Not loaded on every task.

## Maintaining these files

- Add a rule only if a reviewer could check it with a yes/no answer.
- Keep each file under roughly 150 lines. If one grows past that, split it by
  topic (for example `api-security.md`) and add it to the table above.
- When a source document is revised, update the version in the file header and
  re-check the rules that cite it.

## Source versions

| Source | Version used | Last checked |
|---|---|---|
| OWASP Top 10 | 2025 | 2026-11-25 |
| OWASP ASVS | 5.0 | 2026-11-25 |
| NIST SP 800-63B | Rev. 4 | 2026-11-25 |
| NIST SP 800-53 | Rev. 5 | 2026-11-25 |
| NIST SP 800-218 (SSDF) | 1.1 (final, Feb 2022). 1.2 is a public draft (Dec 2025); re-check when it is finalized | 2026-11-25 |
| NIST SP 800-218A (SSDF profile for generative AI) | Final, July 2024 | 2026-11-25 |

Notes from the 2026-11-25 check:

- OWASP Top 10:2025 categories are published on owasp.org. Some coverage
  called the write-up a release candidate with editorial changes pending, but
  no further changes to the list itself are expected.
- ASVS 5.0 chapters used here: V6 Authentication, V7 Session Management,
  V8 Authorization, V9 Self-contained Tokens. These are renumbered from 4.0.3,
  where authentication was V2.
- NIST 800-63B-4 was published as final in July 2025. Its 15-character rule
  is a "SHALL" (mandatory), not a recommendation.
