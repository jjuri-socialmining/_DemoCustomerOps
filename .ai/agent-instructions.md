# Instructions for AI Agents

This repository is public and worked on by both humans and AI coding assistants
(GitHub Copilot, Claude Code, Codex, Cursor, etc.). Follow these rules:

1. **Never expose secrets.** Do not commit `.env` files, API keys, tokens,
   credentials, or certificates. If you discover one already committed, flag it
   immediately and do not just delete it from the latest commit — secrets in
   git history need rotation, not just removal.
2. **No destructive changes without a backup or explanation.** Don't delete
   files without explaining why, and prefer reversible operations.
3. **Explain relevant changes.** Summarize what changed and why in commit
   messages and PR descriptions — don't leave silent behavioral changes.
4. **Keep commits small and clear.** One logical change per commit where
   practical; avoid bundling unrelated work.
5. **Respect the existing GitOps structure.** This repo follows conventions
   from the shared bootstrap tooling (`main` as default branch, `.gitignore`
   patterns for secrets/build artifacts, governance docs). Don't restructure
   directories without a clear reason.
6. **Document changes in README when they affect usage.** If a change affects
   how someone uses `web/`, GitHub Pages, or the repo setup, update the root
   `README.md` (and `web/README.md` if relevant) in the same change.
7. **`web/` is public-facing.** Anything added there is published via GitHub
   Pages. Treat it as production content, not scratch space.

See [`repo-context.md`](./repo-context.md) for what this repository is and how
it's organized.
