#!/bin/sh
# Verify BUZZ prerequisites for every control-room profile. Never prints secrets.
# Requires: BUZZ_RELAY_URL in env or per-profile .env.
set -eu

ROLES="orchestrator product-strategist architect builder quality-guardian self-improver"
RELAY="${BUZZ_RELAY_URL:-}"

fail() { printf '%s\n' "[buzz] ERROR: $*" >&2; exit 1; }
log() { printf '%s\n' "[buzz] $*"; }

hermes --version >/dev/null 2>&1 || fail "hermes CLI not found"

for role in $ROLES; do
  name="hermes-$role"
  home="$(hermes profile path "$name" 2>/dev/null || printf '%s\n' "$HOME/.hermes/profiles/$name")"
  env_file="$home/.env"
  cfg="$home/config.yaml"

  [ -d "$home" ] || fail "$name: profile not found (run profiles.sh first)"
  [ -f "$env_file" ] || fail "$name: missing $env_file (add BUZZ_PRIVATE_KEY)"

  grep -q '^BUZZ_PRIVATE_KEY=' "$env_file" \
    || fail "$name: BUZZ_PRIVATE_KEY not set in $env_file"
  grep -q '^BUZZ_RELAY_URL=' "$env_file" || [ -n "$RELAY" ] \
    || fail "$name: BUZZ_RELAY_URL not set (env or $env_file)"

  # Key uniqueness guard: two profiles must never drive one Buzz identity.
  for other in $ROLES; do
    [ "$other" = "$role" ] && continue
    ohome="$(hermes profile path "hermes-$other" 2>/dev/null || printf '%s\n' "$HOME/.hermes/profiles/hermes-$other")"
    [ -f "$ohome/.env" ] || continue
    if [ "$(grep '^BUZZ_PRIVATE_KEY=' "$env_file")" = "$(grep '^BUZZ_PRIVATE_KEY=' "$ohome/.env" 2>/dev/null || true)" ]; then
      fail "$name and hermes-$other share a BUZZ_PRIVATE_KEY — generate a unique identity per profile"
    fi
  done

  if [ -f "$cfg" ] && grep -q 'buzz:' "$cfg"; then
    log "$name: gateway buzz block present"
  else
    log "$name: WARNING no buzz block in $cfg — add gateway.platforms.buzz (see buzz-handoff.md)"
  fi

done

# Relay reachability (best effort; ws:// relays may not answer plain HTTP).
case "${RELAY:-$(grep -h '^BUZZ_RELAY_URL=' "$HOME/.hermes/profiles/hermes-orchestrator/.env" 2>/dev/null | cut -d= -f2)}" in
  http*) log "relay URL looks HTTP(S) — assume community gateway; skipping probe" ;;
  ws*|wss*) log "relay URL is websocket — probe skipped (use buzz CLI or desktop to verify join)" ;;
  *) log "relay URL unknown — set BUZZ_RELAY_URL to verify" ;;
esac

log "done"
