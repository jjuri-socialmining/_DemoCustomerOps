# DemoCustomerOps

Public repository for orchestration work, automation tooling, and published
web deliverables for this project. Built around the **WAT** pattern
(Workflows, Agents, Tools): markdown SOPs describe what to do, an AI agent
coordinates execution, and deterministic scripts do the actual work.

This repository is **public**. See [Security](#security) before committing
anything.

## Structure

| Path | Purpose |
|---|---|
| `web/` | Public web workspace — published to GitHub Pages |
| `workflows/` | Markdown SOPs (objective, inputs, tools, edge cases) |
| `tools/` | Deterministic scripts that execute the work |
| `tmp/` | Disposable intermediates, not committed |
| `.github/` | GitHub Pages workflow, issue/PR templates |
| `.ai/` | Instructions and context for AI coding assistants |

## Public Web Workspace

Everything placed inside `web/` is published automatically via GitHub Pages
whenever `main` changes under `web/**`. Use it for demos, documentation,
deliverables, and progress updates that should be shareable by URL.

To publish something new:

1. Add your file(s) under `web/pages/`, `web/projects/`, `web/demos/`, or
   `web/assets/` (see `web/README.md` for what goes where).
2. Link to it from `web/index.html` if it should be discoverable from the
   landing page.
3. Commit and push to `main` — `.github/workflows/deploy-web.yml` redeploys
   automatically. You can also trigger it manually from the Actions tab
   (`workflow_dispatch`).

Pages should work standalone (open the file directly in a browser) and when
served by GitHub Pages — no required build step or external dependencies.

## Working with AI assistants

This repo is set up to be worked on by AI coding assistants (GitHub Copilot,
Claude Code, Codex, Cursor, etc.) alongside humans. See
[`.ai/agent-instructions.md`](.ai/agent-instructions.md) for the rules any
agent should follow here, and [`.ai/repo-context.md`](.ai/repo-context.md)
for a fuller summary of the repo's purpose and structure.

## Security

This is a **public** repository. Never commit:

- `.env` / `.env.*` files or any real secrets, API keys, or tokens
- Credentials, certificates, or private keys
- Confidential business or client documents

`.gitignore` enforces the common cases, but review `git status` /
`git diff --cached` before every commit. If you find a secret already
committed, rotate it — removing it from the latest commit is not enough
since it remains in git history.

## Basic Git commands

```bash
git status                 # see what's changed
git add <file>              # stage specific files (avoid `git add -A`)
git commit -m "message"     # commit staged changes
git push                    # push to origin/main
git pull                    # sync with origin/main
```
