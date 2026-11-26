# Identity and access standards

Scope: signing keys, credentials, identity, access boundaries and deployment. Read the applicable section; future account requirements do not authorize implementing accounts. Sources and versions: [reference index](reference/README.md#sources).

## Applies today

The app is single-owner and loopback-only, without application sign-in, roles or user sessions. It **does** use HMAC-signed feedback snapshots and a local signing key. Those establish record integrity, not authenticated identity or authorization between users. Do not describe loopback, Origin checks or signing as a substitute for login.

- **IAM-01 [Project; adapted NIST AC-6/IA-5]** Keep the local access boundary under SEC-30. For changes touching keys/storage, inspect access needs and avoid broadening OS or application access to local research/reviews. A scoped local design does not imply that every process on the computer is trusted or every permission was audited.
- **IAM-03 [Project; adapted NIST IA-5/OWASP A04]** Treat the feedback signing key as secret. Keep it in the ignored local feedback store, never Git, logs, displayed summaries or external providers. Do not regenerate it as an incidental refactor: replacement invalidates outstanding review receipts. Record the owner, purpose, storage/access assumptions and a deliberate replacement/recovery decision when changing its lifecycle. Ramon is the application owner; no automatic rotation mechanism is claimed.
- **IAM-04 [Project]** Preserve signature validation and binding to the original search snapshot when changing feedback. Reuse standard HMAC primitives; do not treat signed evidence metadata as a login token. The system makes no multi-user authorization promise today.

## Before enabling an external provider

- **IAM-40 [Conditional; adapted NIST AC-6/IA-5]** Obtain the owner's provider choice and SEC-23 data-flow decision. Explicitly select credential storage (environment injection or OS keychain/secrets manager), owner, minimum permissions/project scope, revocation/replacement procedure and expiry where supported. Do not assume a provider supports short-lived credentials or that environment variables provide a complete lifecycle solution. Document variable names with empty placeholders only; actual credentials never belong in the repo or browser assets.
- **IAM-42 [Conditional; adapted NIST AU-2/AU-3/IA-5]** Define which credential/security events are recorded, their retention and safe metadata before enabling the integration. Never log a credential, request body or PDF content. Review compromise-triggered replacement and provider-specific credential limitations; do not invent a mandatory rotation interval.

## Before remote or multi-user access

- **IAM-30 [Conditional; adapted OWASP ASVS V6/V7/V8 and NIST AC-3/AC-6]** Obtain an explicit architecture/exposure decision first. Review managed identity-provider or maintained-library authentication, HTTPS, deny-by-default server-side authorization and object-level access checks on every protected route. Define users/roles, document/review isolation, session expiry/revocation, browser request protections and failure behavior. Do not build a new authentication/token protocol. Do not claim the present single-user HTTP server meets this deployment bar.
- **IAM-20 [Conditional; adapted NIST 800-63B-4/IA-2]** Select required assurance and phishing-resistant MFA for privileged remote access as part of the identity-provider design. Password/session policies apply only when those mechanisms exist; consult current source requirements then rather than installing unused authentication now.
- **IAM-41 [Conditional; adapted ASVS V9]** If an integration uses JWTs, use a maintained validator and enforce allowed algorithms, signature, issuer, audience and expiry as appropriate to the protocol. Do not apply JWT requirements to our HMAC review format as though the two were interchangeable.
- **IAM-50 [Conditional; adapted NIST AU-2/AU-3 and OWASP A09]** Define sanitized authentication, authorization and privilege-change auditing before remote access. Include event/time/actor/decision metadata needed for investigation, without credentials or raw research/user content. A local diagnostics log alone is not a completed security audit trail.

## Checklist

- [ ] Applicable scope is identified: current signing/local access, provider credentials, or remote accounts.
- [ ] Key purpose, access assumptions and lifecycle effects are understood; no secret is staged or logged (IAM-01/03/04).
- [ ] Provider choice, storage, ownership, permissions and revocation are decided before use (IAM-40/42, when applicable).
- [ ] Remote identity, transport, authorization, sessions, assurance and safe audit design are reviewed before exposure (IAM-20/30/41/50, when applicable).
- [ ] Conditional items are marked not applicable where appropriate; no nonexistent protection or completed audit is claimed.
