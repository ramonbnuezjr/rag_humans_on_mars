# Identity and Access Management (IAM) Standards

Scope: any code that signs users in, issues or checks tokens, stores
credentials, decides who may do what, or calls another system with a
credential.

Sources:

- `800-63B` — NIST SP 800-63B-4, Digital Identity Guidelines: Authentication
- `800-53 AC-x / IA-x` — NIST SP 800-53 Rev. 5 control families
- `ASVS Vx` — OWASP Application Security Verification Standard 5.0 chapter
- `OWASP-A0x` — OWASP Top 10:2025 category

## Build vs. buy

- **IAM-01** Do not write your own authentication, session, or token-signing
  logic. Use the organisation's identity provider (OIDC / SAML) or a
  maintained library. *(ASVS V6, V9)*

## Passwords (only if this system stores them at all)

- **IAM-10** Minimum length 15 characters when the password is the only
  factor; 8 when it is one factor of MFA. Allow at least 64 characters and
  all printable characters, including spaces. *(800-63B)*
- **IAM-11** No composition rules ("must include a symbol") and no forced
  periodic rotation. Force a change only on evidence of compromise.
  *(800-63B)*
- **IAM-12** Check new passwords against a list of known-breached and common
  passwords. *(800-63B)*
- **IAM-13** Store passwords only as salted hashes from a memory-hard
  algorithm (Argon2id preferred; scrypt or bcrypt acceptable). Never
  reversible encryption. *(ASVS V6; OWASP-A04)*
- **IAM-14** Allow paste and password managers in password fields. *(800-63B)*

## Multi-factor and sessions

- **IAM-20** Require MFA for administrative and privileged access. Prefer
  phishing-resistant authenticators (FIDO2/WebAuthn, passkeys, PIV) over SMS
  or email codes. *(800-63B; 800-53 IA-2)*
- **IAM-21** Rate-limit and lock out repeated failed sign-ins. *(800-63B;
  800-53 AC-7)*
- **IAM-22** Session tokens are random, sent only over HTTPS, set `Secure`,
  `HttpOnly`, and `SameSite` cookies, and are invalidated on sign-out and on
  privilege change. *(ASVS V7)*
- **IAM-23** Enforce both an idle timeout and an absolute session lifetime,
  shorter for privileged sessions. *(800-53 AC-12)*

## Authorization

- **IAM-30** Deny by default. Every endpoint and function that touches
  protected data checks authorization on the server side, on every request.
  *(OWASP-A01 Broken Access Control; ASVS V8)*
- **IAM-31** Check access to the specific object, not just the route
  (user A must not read record 123 by changing an ID in the URL).
  *(OWASP-A01)*
- **IAM-32** Least privilege: users, service accounts, and API keys get only
  the permissions the task needs. No shared accounts. *(800-53 AC-6)*
- **IAM-33** Separation of duties: the identity that requests a privileged
  change is not the one that approves it. *(800-53 AC-5)*

## Machine identities and tokens

- **IAM-40** Service-to-service calls use short-lived credentials (workload
  identity, OAuth client credentials) instead of long-lived static keys
  where the platform supports it. *(800-53 IA-5)*
- **IAM-41** Validate every JWT: signature, `alg` against an allow-list (never
  `none`), issuer, audience, and expiry. *(ASVS V9)*
- **IAM-42** Credentials have an owner and an expiry, and can be revoked
  without a code change. *(800-53 IA-5)*

## Audit

- **IAM-50** Log sign-in success and failure, MFA events, privilege changes,
  and access denials, with who, what, when, and from where. Never log the
  credential itself. *(800-53 AU-2; OWASP-A09)*

## Checklist (run after every task that touches identity or access)

- [ ] No home-grown auth or token signing (IAM-01)
- [ ] Every new endpoint has a server-side, object-level authorization check
      (IAM-30, IAM-31)
- [ ] New roles, keys, or service accounts are least-privilege and owned
      (IAM-32, IAM-42)
- [ ] Tokens fully validated (IAM-41)
- [ ] Security-relevant events logged without secrets (IAM-50)
