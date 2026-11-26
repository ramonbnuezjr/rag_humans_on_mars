# Coding Standards

Scope: all application code in this repository. Default language is Python;
add a section per language if the repo uses others.

Rule IDs are stable. Do not renumber; retire a rule by marking it `RETIRED`.

## Process

- **CODE-01** Write or update tests before or alongside the code they cover.
  Core logic targets at least 90% line coverage.
- **CODE-02** Every change that alters behaviour gets an entry in
  `docs/changelog.md`.
- **CODE-03** Generate complete, runnable code. No placeholders such as
  "add logic here". If the task cannot be finished without more context, stop
  and say what is missing.
- **CODE-04** Never present a mock, stub, or fake implementation as working
  code. Label it as such in the code and in the summary.
- **CODE-05** Ask before deleting files, changing architecture, or adding a
  dependency. Record architecture changes in `docs/architecture.md` first.

## Style (Python)

- **CODE-10** Follow PEP 8. `snake_case` for functions and variables,
  `CapWords` for classes, `UPPER_CASE` for constants.
- **CODE-11** Black formats the code (88-character lines). Ruff lints it.
  Their output is final.
- **CODE-12** Import order: standard library, then third-party, then local, one
  blank line between groups.
- **CODE-13** Compare to `None` with `is` / `is not`, never `==`.

## Types and documentation

- **CODE-20** Every function signature and public method has type hints. Code
  passes `mypy --strict`.
- **CODE-21** Data that crosses a system boundary (HTTP, files, queues, LLM or
  MCP tool output) is parsed into a Pydantic model before use.
- **CODE-22** Every public module, class, and function has a docstring: one-line
  summary, blank line, then Args, Returns, Raises.

## Dependencies

- **CODE-30** Pin every dependency to an exact version in `pyproject.toml`.
- **CODE-31** Add a new dependency to `pyproject.toml` in the same change that
  first imports it.

## Errors and logging

- **CODE-40** Catch exceptions at the boundary (API handler, CLI entry point),
  not deep inside the logic. Let them propagate internally.
- **CODE-41** Every `except Exception` carries a comment explaining why a broad
  catch is justified.
- **CODE-42** Use structured logging (structlog, or stdlib logging with a JSON
  formatter). No `print` for operational output.

## AI models

- **CODE-50** Model names come from configuration or constants, never string
  literals scattered through production code.
- **CODE-51** Handle rate-limit and token-limit errors from model APIs
  explicitly.

## Checklist (run after every task)

- [ ] Tests written or updated; they pass locally (CODE-01)
- [ ] Black, Ruff, and `mypy --strict` pass (CODE-11, CODE-20)
- [ ] No placeholders or unlabeled stubs (CODE-03, CODE-04)
- [ ] New dependencies pinned (CODE-30, CODE-31)
- [ ] Changelog updated if behaviour changed (CODE-02)
