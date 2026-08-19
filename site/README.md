# Forge website (`site/`)

Static landing page and distribution artifacts for Hermes Agents Forge.
No build step, no backend, no dependencies. Deployable on Vercel as-is.

Production domain: **hermes-agents-forge.vercel.app** (configured in `script.js`, `public/install.sh`,
`public/SKILL.md`, `public/start.md`, `public/llms.txt`,
`public/.well-known/skills/index.json` — one constant per file).

## Customer activation

The page has two copy actions:

- **Desktop prompt** — paste into Hermes Desktop chat. Must not contain a raw
  `https://…/SKILL.md` link. Desktop rewrites those as `@url:` and may wrap
  them in backticks, which bash treats as command substitution. The prompt
  builds the URL with `printf` and forbids browser automation.
- **Terminal command** — `hermes skills install https://hermes-agents-forge.vercel.app/SKILL.md --name forge`

Do not present a bare `hermes skills install …` URL command as the Desktop CTA.

After install, the customer describes their goal in plain language. `/forge` is optional and must not be required. `/goal` is never an alias.

The installable skill is also mirrored at `skills/forge/SKILL.md` for GitHub tap layout.

## Layout

- `index.html`, `styles.css`, `script.js` — the landing page.
- `public/` — machine-readable artifacts served at the domain root via the
  rewrites in `vercel.json`:
  - `/SKILL.md` — canonical installable Forge skill (primary artifact).
  - `/start.md` — agent-facing onboarding instructions.
  - `/llms.txt` — short agent-readable index.
  - `/install.sh` — optional compatibility wrapper (not the preferred path).
  - `/.well-known/skills/index.json` — machine-readable skill index.

## Deploy on Vercel

1. Import the repository, set the project root directory to `site/`.
2. Framework preset: **Other**. No build command. Output directory: default (`.`).
3. Deploy. Then verify:
   - `curl -sI https://hermes-agents-forge.vercel.app/SKILL.md` returns `content-type: text/markdown`.
   - `curl -sI https://hermes-agents-forge.vercel.app/start.md` returns `content-type: text/markdown`.
   - `curl -sI https://hermes-agents-forge.vercel.app/llms.txt` returns `content-type: text/plain`.
   - `curl -s https://hermes-agents-forge.vercel.app/.well-known/skills/index.json` returns JSON.

## Release checklist

- [x] Domain set to `hermes-agents-forge.vercel.app` in all six places.
- [ ] `FORGE_VERSION` bumped in `public/install.sh` and
      `public/.well-known/skills/index.json` when cutting a release.
- [ ] `PINNED_SHA256` in `public/install.sh` set to the sha256 of the published
      `public/SKILL.md` (`shasum -a 256 public/SKILL.md`), and the same value
      recorded in `index.json`.
- [ ] No secrets anywhere (`grep -ri "token|secret|apikey|api_key" .`).
