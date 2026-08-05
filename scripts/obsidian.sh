#!/bin/sh
# Verify/seed the shared Obsidian brain for the control room.
# Requires OBSIDIAN_VAULT_PATH (default: ~/obsidian/control-room).
set -eu

VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/obsidian/control-room}"

log() { printf '%s\n' "[obsidian] $*"; }

if [ ! -d "$VAULT/.obsidian" ]; then
  log "WARNING: $VAULT does not look like an Obsidian vault (no .obsidian dir)."
  log "Create it in Obsidian first, or re-run with OBSIDIAN_VAULT_PATH set."
  exit 1
fi

# Canonical control-room structure. Folders are stable; notes are seeded only
# when missing so re-runs never clobber agent-written content.
for d in 00-Inbox 10-Tasks 20-Decisions 30-RunLog 40-Reference; do
  mkdir -p "$VAULT/$d"
done

seed() {
  path="$1"; shift
  [ -f "$VAULT/$path" ] && { log "exists: $path"; return; }
  cat > "$VAULT/$path"
  log "seeded: $path"
}

seed "_control-room.md" <<'EOF'
# Control Room Brain

Shared memory for the Hermes isolated-profile control room.

- `00-Inbox/` — raw requests captured by the orchestrator before normalization.
- `10-Tasks/` — one note per `task_id`; the full payload that BUZZ envelopes
  reference via `payload_ref`.
- `20-Decisions/` — architect decisions (deterministic / agentic / hybrid) with rationale.
- `30-RunLog/` — append-only execution log per task; quality-guardian verdicts land here.
- `40-Reference/` — durable knowledge promoted by the self-improver after approval.

Rules: write-through, never delete, one task one note, secrets never in notes.
EOF

seed "10-Tasks/_template.md" <<'EOF'
---
task_id:
stage: intake
requester:
created_at:
---
# Task <task_id>

## Request
## Brief
## Design
## Build result
## Review verdict
## Delivery
EOF

# Point every profile at the vault (non-secret config only).
ROLES="orchestrator product-strategist architect builder quality-guardian self-improver"
for role in $ROLES; do
  name="hermes-$role"
  home="$(hermes profile path "$name" 2>/dev/null || printf '%s\n' "$HOME/.hermes/profiles/$name")"
  [ -d "$home" ] || continue
  env_file="$home/.env"
  touch "$env_file"
  if grep -q '^OBSIDIAN_VAULT_PATH=' "$env_file"; then
    log "$name: OBSIDIAN_VAULT_PATH already set"
  else
    printf 'OBSIDIAN_VAULT_PATH=%s\n' "$VAULT" >> "$env_file"
    chmod 600 "$env_file"
    log "$name: OBSIDIAN_VAULT_PATH -> $VAULT"
  fi
done

log "done"
