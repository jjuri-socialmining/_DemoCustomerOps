# web/

Public web workspace for this repository. Everything in this folder is published
to GitHub Pages from the `main` branch via `.github/workflows/deploy-web.yml`.

## Structure

- `index.html` — landing page, linked from GitHub Pages root.
- `pages/` — standalone documentation or informational pages.
- `projects/` — project-specific deliverables and writeups.
- `demos/` — interactive demos and prototypes.
- `assets/` — shared images, styles, and static resources.

## Publishing something new

1. Add your HTML/static files under the relevant subfolder (or `web/` root for
   one-off demos, following the existing pattern).
2. Link to it from `index.html` if it should be discoverable from the landing page.
3. Commit and push to `main` — the deploy workflow republishes `web/` automatically.

## Rules

- No secrets, API keys, tokens, or credentials in anything placed here — this
  folder is public.
- No external build step is required; pages should work by opening the file
  directly in a browser as well as when served by GitHub Pages.
