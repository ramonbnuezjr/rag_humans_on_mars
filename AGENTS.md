# Project guidance

## Purpose and stage

Build a source-grounded research assistant about humans reaching, inhabiting, and thriving on Mars. The owner is learning software development through hands-on work and has an operations background. Explain consequential decisions plainly and keep changes small enough to inspect.

Read `README.md`, `status.md`, and [the standards index](standards/README.md) first, then the standards applicable to the task. Use the current status to distinguish implemented evidence retrieval from planned generated answers and automatic evidence assessment.

## Commands

- Inventory: `PYTHONPATH=src python3 -m mars_rag inventory`
- Syntax check: `python3 -m compileall -q src`
- Tests: `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests`
- Browser JavaScript syntax, when changed: `node --check src/mars_rag/web_static/app.js`

Run commands from the repository root. If system Python cannot run, use `.venv/bin/python` for Python commands. Runtime compatibility and tooling decisions are recorded in the coding standard; do not silently upgrade them.

## Authoritative standards

- [Coding](standards/coding-standards.md): implementation, tests, provenance, scope and change records.
- [Security](standards/security-standards.md): trust boundaries, local serving, source preservation, privacy and provider data transfer.
- [IAM](standards/iam-standards.md): current signing-key safeguards and conditional requirements for credentials, accounts or remote access.

Each detailed rule has one authoritative home. Apply the scope and conflict procedure in the index; do not replace it with a blanket "stricter wins" rule. `CLAUDE.md` remains a relative symlink to this file. Keep progress history in `status.md`, not here.
