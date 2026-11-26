# Development and pull request workflow

Treat the project folder as one Git repository. Do not initialize `coding_projects` as the repository containing all future projects.

The owner selected [ramonbnuezjr/rag_humans_on_mars](https://github.com/ramonbnuezjr/rag_humans_on_mars) as the remote. The local repository was initialized on 2026-11-22 after confirming that remote was empty. Use the existing repository going forward; the bootstrap example below is historical setup guidance, not a command sequence to repeat on an existing checkout. Raw PDFs and generated outputs are intentionally absent from GitHub; a fresh clone will not contain the locally searchable corpus.

## First local commit

After the scaffold is installed, run these commands from the project root. If the directory is already a repository, use its existing history instead of initializing another repository.

```sh
git init -b main
git status --short
git add README.md AGENTS.md CLAUDE.md status.md pyproject.toml .gitignore .env.example src docs sources evals tests data .github
git diff --cached --stat
git diff --cached
git commit -m "Scaffold Humans on Mars research project"
```

The ignore rules exclude PDFs and generated data. Inspect the actual staged diff before committing. The scaffold installer does not run these Git commands or publish anything.

## A first feature branch

```sh
git switch -c feature/pdf-extraction
```

Implement extraction for one document. Check page references and representative text. Add a small reusable fixture only if you can redistribute it. Update `status.md`, commit the feature, and review the diff.

Once you have created and connected a GitHub repository, push `main` and the feature branch to that remote and open a pull request from the feature branch into `main`. You can author and review your own pull requests; use them to record the change and its evidence.

## Pull request contents

Explain what behavior changed, how it was checked, and any remaining limitations. Example: “Extracts page text from one PDF while retaining source ID and one-based PDF page numbers. Checked against five manually reviewed pages; table extraction is still incomplete.”

## Current checks

```sh
python3 -m compileall -q src
PYTHONPATH=src python3 -m mars_rag inventory
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
node --check src/mars_rag/web_static/app.js
```

Thirty-four software tests passed on 2026-11-22, covering extraction, indexing, HTTP routes, local diagnostic logging and persistent evidence reviews. Install the optional extraction dependencies before running the synthetic-PDF suite; HTTP integration tests need permission to bind loopback sockets. Node is only needed for the optional JavaScript syntax check, not to run the UI. See [test details](../tests/README.md). Draft research questions and agent-reviewed retrieval checks are not independent answer-quality evaluations.

## Shared assistant instructions

Start with [AGENTS.md](../AGENTS.md) and the [standards index](../standards/README.md); detailed rules have one authoritative home. Follow the scoped coding, security and IAM rules applicable to the change. Tool/runtime migrations and dependency additions are explicit decisions, not prerequisites silently introduced by the standards. See [the adoption record](decisions/2026-11-25-project-standards.md).

`AGENTS.md` is the actual file. `CLAUDE.md` is a relative symbolic link to `AGENTS.md`, so both entry points read the same instructions. Edit `AGENTS.md` directly; do not replace the link with a copy. Git can track the link. A Windows checkout may require symlink support; with `core.symlinks=false`, Git checks it out as a small text file containing the target path instead.

Check locally with `ls -l CLAUDE.md` and `readlink CLAUDE.md`. The expected link target is `AGENTS.md`.
