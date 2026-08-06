# obsidian-policy.md — Hermes + Obsidian Safety & Access Rules

This policy defines how Hermes and its specialist roles may interact with an Obsidian vault. It complements `shared/safety-gates.md` and `shared/context-policy.md` by adding vault-specific guardrails.

## Scope

- Applies to all Hermes profiles and skills that read or write Obsidian notes.
- Assumes the vault is accessed via the **Obsidian Local REST API** plugin (`coddingtonbear/obsidian-local-rest-api`).
- Assumes `OBSIDIAN_VAULT_PATH` and `API_SERVER_KEY` are configured in `${HERMES_HOME:-~/.hermes}/.env`.

## Vault layout

- **Scoped folder** (default: `/Hermes` or `/Agent Memory`) — the only directory Hermes is allowed to write to by default.
- **Private folders** — any folder outside the scoped folder, e.g. `/Personal`, `/Work`, `/Secrets`.
- **Read-only shared folders** — optional folders Hermes may read but not modify, e.g. `/Reference`, `/Docs`.

## Access tiers

| Tier | Description | Allowed operations | Example paths |
|------|-------------|--------------------|---------------|
| **Private** | Sensitive or personal notes. Hermes must not touch these unless explicitly configured. | None (no read, no write) | `/Personal`, `/Secrets`, `/Finance` |
| **Read-only** | Reference material Hermes may use for context but must not alter. | Read only | `/Reference`, `/Docs`, `/Templates` |
| **Scoped (Hermes)** | Dedicated folder for Hermes-generated notes, memory, and agent artifacts. | Read + write (create, update, delete) | `/Hermes`, `/Agent Memory` |

Skills should be configured with explicit allowlists for read-only and scoped paths. Private paths must be denylisted by default.

## Secrets and credentials

- **Never store secrets, API keys, or credentials in Obsidian**, even in the scoped folder.
- Sensitive data must live in Hermes' native secret store or environment variables, not in Markdown notes.
- Skills must not generate or echo secrets into note content.

## Docker / remote Hermes

- If Hermes runs in Docker or on a remote host, the vault path must be mounted explicitly (e.g. `-v "$OBSIDIAN_VAULT_PATH:$OBSIDIAN_VAULT_PATH:ro"`).
- For write access, prefer mounting only the scoped folder as read-write (`-v "$SCOPED_DIR:$SCOPED_DIR:rw"`), leaving the rest of the vault read-only or unmounted.
- Ensure the container can reach the Obsidian REST API (host network or explicit port mapping).

## Smoke test & validation

After initial setup:

1. Run `scripts/obsidian.sh` to create a smoke test note.
2. Verify the note appears in Obsidian under the scoped folder.
3. Confirm no notes are created outside the scoped folder.
4. Periodically re-run the smoke test after major config changes.

## Skill-level enforcement

Skills that interact with Obsidian should:

- Use `OBSIDIAN_VAULT_PATH` from the env and never hardcode paths.
- Validate target paths against allowed read-only and scoped allowlists before any REST call.
- Fail loudly (and refuse to write) if a path resolves outside allowed directories (e.g. via `..` traversal).
- Log which tier (private / read-only / scoped) each operation targets, for auditability.

## Relationship to other policies

- `safety-gates.md` — general approvals, safety, and honest reporting.
- `context-policy.md` — compact handoffs and anti-bloat rules (applies to note content too).
- This file — vault-specific access control and secret handling.

## Example allowlist config (for a skill)

```yaml
obsidian:
  vault_path_env: OBSIDIAN_VAULT_PATH
  api_key_env: API_SERVER_KEY
  read_only_paths:
    - Reference
    - Docs
    - Templates
  scoped_paths:
    - Hermes
    - Agent Memory
  private_paths_denylist:
    - Personal
    - Secrets
    - Finance
```

Skills should enforce these at runtime, not just in documentation.
