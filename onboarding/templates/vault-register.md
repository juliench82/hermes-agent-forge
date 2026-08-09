# Vault Register — install-time

> Durable record of the Obsidian vault choice made during Control Room install.
> Path and policy only. Never store API keys, plugin tokens, or note contents here.

## Resolution

- Status: ACCEPTED | CREATED | SKIPPED | PENDING
- Resolved at: <ISO-8601 timestamp>
- Host OS: macOS | Linux | Windows | other
- Resolution method: env | hermes-env | cwd | discovered | user-path | create | skip

## Path

- OBSIDIAN_VAULT_PATH (absolute): <path or none>
- Suggested path shown to user: <path>
- CREATE default offered: <path>
- `.obsidian/` present at resolve time: yes | no | n/a

## Access mode

- Mode: local-files | rest-api | both | none
- Scoped write folder: <e.g. Hermes>
- Read-only folders (optional): <list>
- Private / denied folders (optional): <list>

## Local map

- `.hermes.md` at vault root: present | seeded | absent | n/a
- Seed source: `onboarding/templates/hermes-md.md` | custom | none

## Env wiring

- Written to `${HERMES_HOME}/.env`: yes | no
- Written to native profile `.env` files: yes | no | partial | n/a
- `scripts/obsidian.sh` run after resolve: yes | no | skipped

## Notes

- <optional operator notes; no secrets>

## Rules

- SKIP is a valid outcome; do not treat it as install failure by itself.
- Changing the vault path later is a material install change: re-run this workflow and update this register.
- Credentials for Local REST API stay in the approved env/secret store, never in this file.
