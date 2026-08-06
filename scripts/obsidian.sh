#!/usr/bin/env bash
# obsidian.sh — Hermes + Obsidian integration bootstrap
#
# Goals:
# - Install/check Obsidian Local REST API plugin (coddingtonbear/obsidian-local-rest-api)
# - Configure Hermes env: OBSIDIAN_VAULT_PATH and API_SERVER_KEY
# - Create a scoped vault folder for Hermes (e.g. /Hermes or /Agent Memory)
# - Provide Docker mount guidance if HERMES_DOCKER=1
# - Run a smoke test (write a harmless Markdown note)
#
# Usage:
#   ./scripts/obsidian.sh
#
# Prerequisites:
# - Obsidian installed and a vault open
# - Hermes installed (~/.hermes or $HERMES_HOME)
# - curl or wget available
# - (Optional) Docker, if HERMES_DOCKER=1

set -euo pipefail

# === Configurable vars ===
OBSIDIAN_VAULT_PATH="${OBSIDIAN_VAULT_PATH:-}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
OBSIDIAN_REST_PORT="${OBSIDIAN_REST_PORT:-8642}"
OBSIDIAN_REST_HOST="${OBSIDIAN_REST_HOST:-127.0.0.1}"
OBSIDIAN_SCOPED_FOLDER="${OBSIDIAN_SCOPED_FOLDER:-Hermes}"
HERMES_DOCKER="${HERMES_DOCKER:-0}"

# === Helpers ===
log() { printf "[obsidian.sh] %s\n" "$*"; }
die() { log "ERROR: $*"; exit 1; }
ok() { log "OK: $*"; }

# === 1. Validate vault path ===
if [ -z "$OBSIDIAN_VAULT_PATH" ]; then
  die "OBSIDIAN_VAULT_PATH is not set. Set it before running this script, e.g.:
  export OBSIDIAN_VAULT_PATH=\"$HOME/ObsidianVault\"
or in your shell profile / .env file."
fi

if [ ! -d "$OBSIDIAN_VAULT_PATH" ]; then
  die "OBSIDIAN_VAULT_PATH does not exist: $OBSIDIAN_VAULT_PATH"
fi

log "Vault path: $OBSIDIAN_VAULT_PATH"

# === 2. Ensure scoped folder exists ===
SCOPED_DIR="$OBSIDIAN_VAULT_PATH/$OBSIDIAN_SCOPED_FOLDER"
if [ ! -d "$SCOPED_DIR" ]; then
  log "Creating scoped folder for Hermes: $SCOPED_DIR"
  mkdir -p "$SCOPED_DIR"
else
  ok "Scoped folder already exists: $SCOPED_DIR"
fi

# === 3. Check Obsidian Local REST API plugin ===
# We check the plugin's health endpoint. If it fails, we guide the user to install it.
REST_BASE="http://${OBSIDIAN_REST_HOST}:${OBSIDIAN_REST_PORT}"
HEALTH_URL="$REST_BASE/health"

log "Checking Obsidian Local REST API at $HEALTH_URL ..."

if curl -sSf "$HEALTH_URL" >/dev/null 2>&1; then
  ok "Obsidian Local REST API is reachable."
else
  die "Obsidian Local REST API is NOT reachable at $HEALTH_URL.
To fix:
1) In Obsidian: Settings → Community plugins → Browse
2) Install 'obsidian-local-rest-api' by coddingtonbear
3) Enable the plugin and ensure the server is running (default port $OBSIDIAN_REST_PORT)
4) Re-run this script.
If you use a non-default port/host, set OBSIDIAN_REST_PORT and/or OBSIDIAN_REST_HOST before running."
fi

# === 4. Configure Hermes env file ===
HERMES_ENV="$HERMES_HOME/.env"
if [ ! -d "$HERMES_HOME" ]; then
  log "Creating Hermes home directory: $HERMES_HOME"
  mkdir -p "$HERMES_HOME"
fi

# Ensure OBSIDIAN_VAULT_PATH is in the .env file
if [ -f "$HERMES_ENV" ]; then
  if grep -q "^OBSIDIAN_VAULT_PATH=" "$HERMES_ENV"; then
    ok "OBSIDIAN_VAULT_PATH already set in $HERMES_ENV"
  else
    log "Appending OBSIDIAN_VAULT_PATH to $HERMES_ENV"
    printf "\nOBSIDIAN_VAULT_PATH=%s\n" "$OBSIDIAN_VAULT_PATH" >> "$HERMES_ENV"
  fi
else
  log "Creating $HERMES_ENV with OBSIDIAN_VAULT_PATH"
  printf "OBSIDIAN_VAULT_PATH=%s\n" "$OBSIDIAN_VAULT_PATH" > "$HERMES_ENV"
fi

# === 5. Generate API_SERVER_KEY (if not already set) ===
# The REST API plugin uses an API key; we generate one and advise the user to set it in Obsidian.
# We store it locally so Hermes can pick it up.
API_KEY_FILE="$HERMES_HOME/obsidian_api_key"
if [ -f "$API_KEY_FILE" ]; then
  API_SERVER_KEY="$(cat "$API_KEY_FILE")"
  ok "Reusing existing API_SERVER_KEY from $API_KEY_FILE"
else
  # Generate a reasonably strong key
  API_SERVER_KEY="$(openssl rand -hex 16 2>/dev/null || head -c 32 /dev/urandom | xxd -p)"
  printf "%s" "$API_SERVER_KEY" > "$API_KEY_FILE"
  chmod 600 "$API_KEY_FILE"
  log "Generated new API_SERVER_KEY and saved to $API_KEY_FILE"
fi

# Append API_SERVER_KEY to .env if not present
if grep -q "^API_SERVER_KEY=" "$HERMES_ENV"; then
  ok "API_SERVER_KEY already set in $HERMES_ENV"
else
  log "Appending API_SERVER_KEY to $HERMES_ENV"
  printf "API_SERVER_KEY=%s\n" "$API_SERVER_KEY" >> "$HERMES_ENV"
fi

log "Ensure Obsidian's Local REST API plugin is configured with this key:
  API_SERVER_KEY=$API_SERVER_KEY
(You may need to paste it into the plugin's settings in Obsidian.)"

# === 6. Docker guidance (optional) ===
if [ "$HERMES_DOCKER" = "1" ]; then
  log "HERMES_DOCKER=1 detected — Docker mount guidance:"
  log "  Mount your vault path into the Hermes container, e.g.:
    -v \"$OBSIDIAN_VAULT_PATH:$OBSIDIAN_VAULT_PATH:ro\"
  For read-write access to the scoped folder only:
    -v \"$SCOPED_DIR:$SCOPED_DIR:rw\"
  Then inside the container set:
    OBSIDIAN_VAULT_PATH=$OBSIDIAN_VAULT_PATH
  and ensure the container can reach the Obsidian REST API (host network or port mapping)."
fi

# === 7. Smoke test: write a harmless note via REST API ===
SMOKE_NOTE="$OBSIDIAN_SCOPED_FOLDER/00_Hermes_Smoke_Test.md"
SMOKE_PATH="$OBSIDIAN_VAULT_PATH/$SMOKE_NOTE"
SMOKE_URL="$REST_BASE/vault/${SMOKE_NOTE}"

log "Running smoke test: writing $SMOKE_NOTE ..."

SMOKE_CONTENT="# Hermes smoke test

This is a harmless test note created by \`scripts/obsidian.sh\`.
If you see this in Obsidian, the integration is working.

- Created at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- Vault path: $OBSIDIAN_VAULT_PATH
- Scoped folder: $OBSIDIAN_SCOPED_FOLDER
"

# Write via REST API
if curl -sSf -X PUT "$SMOKE_URL" \
  -H "Authorization: Bearer $API_SERVER_KEY" \
  -H "Content-Type: text/markdown" \
  --data-raw "$SMOKE_CONTENT"; then
  ok "Smoke test note created successfully: $SMOKE_NOTE"
else
  die "Smoke test FAILED. Hermes cannot write to Obsidian via the REST API.
Check:
- The Local REST API plugin is enabled and running
- API_SERVER_KEY matches in Obsidian and in $HERMES_ENV
- The REST base URL ($REST_BASE) is correct
- Firewall / CORS / proxy is not blocking the request"
fi

# === Done ===
ok "Hermes + Obsidian integration is ready.
Next steps:
1) Open Obsidian and confirm you see: $SCOPED_DIR
2) In Obsidian, open: $SCOPED_DIR/$SMOKE_NOTE
3) In your Hermes config/skills, use OBSIDIAN_VAULT_PATH and API_SERVER_KEY from:
   $HERMES_ENV
4) Restrict Hermes skills to read/write only within the scoped folder as per shared/obsidian-policy.md
"
