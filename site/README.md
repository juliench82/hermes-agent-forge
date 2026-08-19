# Forge website (`site/`)

Static landing page and distribution artifacts for Hermes Agents Forge.
No build step, no backend, no dependencies. Deployable on Vercel as-is.

Production domain: **hermes-agents-forge.vercel.app**.

## Customer activation

Two copy actions:

- **Desktop prompt** — paste into Hermes Desktop. Builds the URL with `printf`
  (Desktop rewrites raw `https://` links as `@url:`). Writes the skill with
  `curl -o` into `~/.hermes/skills/software-development/forge/SKILL.md`.
  Do not use `hermes skills install` for this URL: community scans false-positive
  on safety wording and block the install (exit code can still be 0).
- **Terminal command** — the same `mkdir` + `curl -o` one-liner.

After the `forge` row appears in `hermes skills list`, the customer describes
their goal. `/forge` is optional. `/goal` is never an alias.

## Layout

- `index.html`, `styles.css`, `script.js` — the landing page.
- `public/` — artifacts served at the domain root via `vercel.json`.
- `skills/forge/SKILL.md` — tap-layout mirror of `public/SKILL.md`.

## Release checklist

- [x] Domain set to `hermes-agents-forge.vercel.app`.
- [ ] `FORGE_VERSION` bumped in `public/install.sh` and `index.json` on release.
- [ ] `PINNED_SHA256` set to the sha256 of published `public/SKILL.md`.
