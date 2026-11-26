# Standards references

Read sources to resolve a specific rule's origin/scope, not as routine task context. This index links authoritative publications; it does not download or redistribute full documents. Accessing a current page does not prove every derived rule has been audited.

## Sources

| Reference | Version and use |
| --- | --- |
| [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | SSDF 1.1, final February 2022; high-level development practices, including PS.1 protection, PW.4 component selection, PW.5 secure coding, PW.8 executable testing and RV.1 vulnerability identification. Tool choices and coverage targets are our own policies. |
| [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications) | Tracks revisions; 1.2 was listed as a draft during the 2026-11-25 discussion. Do not silently substitute draft requirements for the selected baseline. |
| [OWASP Top 10:2025](https://top10.owasp.org/2025/) | Awareness/risk categories: A01 access control/SSRF, A02 misconfiguration, A03 supply chain, A04 cryptography, A05 injection, A08 integrity, A09 logging, A10 exceptional conditions. Category citations explain risk; they are not detailed compliance attestations. |
| [OWASP ASVS](https://asvs.owasp.org/) | Selected 5.0.0 stable release, May 2025; technical verification reference. Identity chapters V6 authentication, V7 sessions, V8 authorization and V9 self-contained tokens inform conditional deployment rules. Select exact applicable requirements when implementing those features. |
| [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) | Control catalogue; AC-3 access enforcement, AC-6 least privilege, IA-2 authentication, IA-5 authenticator management, AU-2 event selection and AU-3 audit content. The publication page notes Release 5.2.0 updates. These are selectively adapted concepts, not adoption of the entire organizational control catalogue. |
| [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) | Authentication/authenticator guidance, final July 2025. Conditional reference for a future identity/assurance design; no password database or application sessions are introduced now. |
| [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final) | Final July 2024, model-development-focused SSDF community profile. Not blanket authority merely because code was AI-assisted. Reassess applicability if actual AI/model development changes the project. |
| [PEP 8](https://peps.python.org/pep-0008/) | Python readability and naming guidance; does not mandate Black, Ruff, mypy or Pydantic. |
| [Python 3.9 lifecycle](https://peps.python.org/pep-0596/) | End of life October 31, 2025. Existing compatibility declarations are retained only pending a separate supported-runtime decision. |

Version/scope review date: 2026-11-25. SSDF, OWASP and NIST publication metadata were consulted during the discussion/adoption; this is not a line-by-line source mapping or compliance assessment. Before a future authentication/provider implementation, inspect the exact current requirements and document applicability.
