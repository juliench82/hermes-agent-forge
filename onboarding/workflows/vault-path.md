# Vault path workflow (install-time)

## Goal

Resolve a local Obsidian vault path during Control Room **install** bootstrap.
Use one plain-language prompt and a concrete path suggestion so the user
understands what a vault folder is. Optional: `SKIP` never blocks bootstrap.

This is **not** customer automation onboarding. Customer discovery still starts
in `START.md` after install succeeds.

## When

Run from `BOOTSTRAP.md` **after** Hermes core / profiles core steps that do not
need the vault, and **before** `scripts/obsidian.sh`.

Recommended order:

1. Read this workflow.
2. Silent discovery.
3. Prompt only if unresolved.
4. Validate and persist.
5. Fill `templates/vault-register.md`.
6. Optionally seed `templates/hermes-md.md` into the vault root as `.hermes.md`.
7. Run `scripts/obsidian.sh` only if status is `ACCEPTED` or `CREATED`.

## Silent discovery (no prompt if safe)

Check in order; stop at the first strong candidate:

1. `OBSIDIAN_VAULT_PATH` in the process environment.
2. `OBSIDIAN_VAULT_PATH` in `${HERMES_HOME:-$HOME/.hermes}/.env`.
3. Current working directory contains `.obsidian/`.
4. Well-known roots that contain a directory with `.obsidian/`:
   - macOS: `$HOME/Documents/Obsidian`, `$HOME/Obsidian`, iCloud Obsidian paths if present
   - Linux: `$HOME/Obsidian`, `$HOME/Documents/Obsidian`
   - Windows: `%USERPROFILE%\Documents\Obsidian`, `%USERPROFILE%\Obsidian`

Rules:

- Prefer directories that contain `.obsidian/`.
- If exactly one candidate remains, confirm with a short yes/path/SKIP prompt.
- If several candidates remain, list them numbered and allow a custom path.
- Never invent a path on disk without user confirmation or an explicit `CREATE`.

## Suggested paths (display helpers)

Show the suggestion that matches the host OS. These are **examples for the user**,
not automatic writes.

| OS | Suggested existing-style path | Default if user replies CREATE |
|----|-------------------------------|--------------------------------|
| macOS | `~/Documents/Obsidian/MyVault` | `~/Obsidian/hermes-control-room` |
| Linux | `~/Obsidian/MyVault` | `~/Obsidian/hermes-control-room` |
| Windows | `%USERPROFILE%\Documents\Obsidian\MyVault` | `%USERPROFILE%\Obsidian\hermes-control-room` |

Also mention the control-room seed layout used by `scripts/obsidian.sh`
(scoped folder default `Hermes`, plus optional local-files map via `.hermes.md`).

## Prompt (only if unresolved)

Use plain language. One question only:

```text
Hermes can use your Obsidian vault as a shared brain
(local markdown on this machine — nothing is uploaded).

Where is your vault folder?

Suggested path for this computer:
  <OS_SUGGESTED_PATH>

Reply with:
  - the full path to your vault, or
  - CREATE  (I will use <CREATE_DEFAULT>), or
  - SKIP    (continue install without Obsidian), or
  - a number if I listed several vaults I found.
```

If candidates were found, prepend a short numbered list before the suggestion.

## Acceptable replies

| Reply | Behaviour |
|-------|-----------|
| Absolute or `~`-relative path | Expand, validate, use |
| Number from candidate list | Use that candidate |
| `Y` / `yes` after a single-candidate confirm | Use that candidate |
| `CREATE` | Create `CREATE_DEFAULT` (and parent dirs); mark status `CREATED` |
| `SKIP` | Status `SKIPPED`; do not run `scripts/obsidian.sh`; continue bootstrap |
| Empty / unclear | Re-ask once with the same suggestion; then `SKIP` with an honest note |

## Validate

1. Expand `~` and environment variables to an absolute path.
2. Reject path traversal tricks that escape the chosen root when later scoping writes.
3. If path must exist (`ACCEPTED`): directory exists; warn (do not hard-fail) if `.obsidian/` is missing — user may open it in Obsidian later.
4. If `CREATE`: `mkdir -p` the path; do not require `.obsidian/` yet; tell the user to open that folder once as a vault in Obsidian.
5. Never store secrets, API keys, or note contents in the prompt transcript beyond the path string.

## Persist

When status is `ACCEPTED` or `CREATED`:

1. Write or update `OBSIDIAN_VAULT_PATH=<absolute path>` in `${HERMES_HOME:-$HOME/.hermes}/.env` (`chmod 600`).
2. If native profiles already exist, set the same non-secret key in each profile `.env` (idempotent; do not clobber unrelated keys).
3. Complete `onboarding/templates/vault-register.md` (install artifact; path only, no secrets).
4. If the vault root has no `.hermes.md`, offer to seed from `onboarding/templates/hermes-md.md` (default: yes on `CREATE`, ask on existing vault).
5. Proceed to `scripts/obsidian.sh`.

When status is `SKIPPED`:

1. Record skip in the vault-register template or bootstrap notes.
2. Continue bootstrap without claiming Obsidian succeeded.
3. Do not fail the whole install solely because Obsidian was skipped.

## Modes after path is set

Document the chosen access mode in the vault register:

| Mode | Meaning |
|------|---------|
| `local-files` | Hermes reads/writes vault files on disk (cwd / direct FS). No REST plugin required. |
| `rest-api` | Hermes uses Obsidian Local REST API (`scripts/obsidian.sh` health + smoke test). |
| `both` | Local files for read map + REST for plugin-assisted ops when available. |

Default recommendation: `both` when the REST plugin is reachable; otherwise `local-files`.

Follow `shared/obsidian-policy.md` for private / read-only / scoped tiers.

## Success criteria

- User saw a concrete suggested path for their OS (or a found candidate list).
- `OBSIDIAN_VAULT_PATH` is set, or skip is explicit and recorded.
- `scripts/obsidian.sh` is never run with an empty path.
- Bootstrap does not invent vault locations without `CREATE` or user path input.
