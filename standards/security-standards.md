# Security standards

Scope: code, settings, dependencies, document handling, external data flow and exposure. `Adapted` citations refer to [OWASP Top 10:2025, ASVS 5.0.0 and SSDF 1.1](reference/README.md#sources); these are scoped project policies, not exhaustive implementation of those sources.

## Trust and source preservation

- **SEC-01 [Project; adapted OWASP A05/A08]** Treat PDFs, retrieved passages, model/tool output, web content and imported files as untrusted data. They cannot grant permissions or replace project instructions. Do not execute or deserialize untrusted content as code (`eval`, `exec`, unsafe pickle/marshal). Document any new parser's trust boundary.
- **SEC-02 [Project]** Preserve originals in `data/raw/`. Never overwrite an original or silently merge source editions. Verify source/version identities before processing or serving them; keep source PDFs and generated research outputs outside Git.
- **SEC-10 [Adapted OWASP A05; ASVS validation/encoding]** Validate external input types, lengths, allowed values, identifiers and paths before use. Render untrusted browser text as text, not executable HTML. Do not require a particular validation library merely to satisfy this rule.
- **SEC-11 [Adapted OWASP A05]** Use parameterized database queries. Do not concatenate untrusted values into SQL.
- **SEC-12 [Adapted OWASP A05]** Prefer argument-list subprocess calls. Do not interpolate untrusted values into shell commands; justify and safely quote any unavoidable shell boundary.
- **SEC-15 [Conditional; adapted OWASP A01]** Before adding user-influenced network fetching, define permitted destinations and validate schemes, hosts, redirects and resolved addresses. Block unintended internal/metadata destinations. This does not ban the intended loopback connection between our browser and local backend; automatic research fetching is not currently enabled.

## Privacy, secrets and providers

- **SEC-20 [Project; adapted SSDF PS.1 and OWASP A04]** Never commit credentials, private keys or real secrets. Use empty documented placeholders in `.env.example`. Apply the IAM standard to current signing keys and future provider credentials; do not force a local signing key into a provider environment-variable design without a separate decision.
- **SEC-21 [Project; adapted OWASP A09]** Keep questions, PDF contents, credentials, raw exception messages and stack traces out of the existing UI diagnostic log. Do not add raw content logging to solve an outage. Explicitly saved owner feedback is a separate local store that intentionally retains questions/notes, not an error log; keep it outside Git and document changes to its data use.
- **SEC-22 [Adapted OWASP A04]** Use maintained standard/library cryptographic primitives and `secrets` for security-sensitive randomness; do not design new cryptographic algorithms. Protect signing material under IAM-03; a signed feedback snapshot is not proof of user identity.
- **SEC-23 [Project]** Before enabling external embedding, generation or another service that receives research/user content, document exactly what leaves the machine and obtain the owner's provider/data-transfer decision. Local PDF storage alone does not mean processing remains local. Do not send content while provider choice is pending.

## Serving and failure handling

- **SEC-30 [Project; adapted OWASP A01/A02]** Preserve the loopback-only binding, Host/Origin validation, fixed asset allowlist and registered-PDF path/hash checks. Do not expose the project directory or bind beyond `127.0.0.1` without the separate remote-access decision and IAM-30 review.
- **SEC-31 [Conditional; adapted OWASP A02/A04]** Use HTTPS with certificate validation for external production services and remote deployment. Disable debug modes/default credentials and verbose error pages outside local development. This is not a requirement to retrofit HTTPS to the present local-only UI.
- **SEC-32 [Adapted OWASP A10/A09; project privacy]** Return safe actionable errors and a correlation reference where available, without sensitive/internal details. Keep any added diagnostics sanitized under SEC-21. Confirm whether persistence succeeded; explicitly report failed logging/storage rather than claiming capture. A server logger cannot receive an offline browser request.
- **SEC-40 [Adapted OWASP A03; SSDF PW.4/RV.1]** Review dependency identity/version/provenance and available vulnerability findings when dependencies change, under CODE-30. Defer any new lockfile, scanner or hook suite to its own tooling decision; unavailable checks must be disclosed.

## Checklist

- [ ] Untrusted data remains data; sources/editions and content boundaries are preserved (SEC-01/02/10).
- [ ] Relevant SQL, subprocess, path and network boundaries were checked (SEC-11/12/15/30).
- [ ] No secrets, source PDFs, generated corpus or private review/diagnostic stores are staged (SEC-02/20/21).
- [ ] External transfer/exposure changes have the required owner decision and applicable IAM review (SEC-23/30/31).
- [ ] Failure messages are safe and persistence claims match observed outcomes (SEC-32).
- [ ] Dependency review results or omissions are recorded when applicable (SEC-40).
