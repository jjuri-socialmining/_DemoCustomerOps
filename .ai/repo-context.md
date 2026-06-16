# Repository Context

## Purpose

Public repository for orchestration work, tooling, and published deliverables
related to this project. It follows the WAT (Workflows, Agents, Tools)
pattern: markdown SOPs in `workflows/`, deterministic scripts in `tools/`, and
an AI agent coordinating between them.

## Structure

- `web/` — public web workspace, deployed to GitHub Pages via
  `.github/workflows/deploy-web.yml` on every push to `main` that touches
  `web/**`.
- `workflows/` — markdown SOPs defining objectives, inputs, tools, and edge
  cases for repeatable tasks.
- `tools/` — deterministic scripts (Python, etc.) that execute the actual
  work described by a workflow.
- `tmp/` — disposable intermediate files, regenerated as needed, not meant to
  be committed.
- `.github/` — GitHub configuration: Pages deploy workflow, issue templates,
  PR template.
- `.ai/` — instructions and context for AI coding assistants working in this
  repo (this folder).

## Workflow

1. Work is described in a `workflows/*.md` SOP.
2. An agent (human or AI) reads the workflow, gathers inputs, and runs the
   appropriate tool(s) in `tools/`.
3. Deliverables meant to be shared go to `web/` (or external cloud services,
   per project convention) — not left as local-only artifacts.
4. Changes affecting `web/` redeploy automatically to GitHub Pages on merge
   to `main`.

## Security posture

This repo is **public**. Secrets, credentials, and confidential business
documents must never be committed — see `.gitignore` for enforced patterns
and [`agent-instructions.md`](./agent-instructions.md) for agent-specific
rules.
