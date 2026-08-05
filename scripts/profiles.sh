#!/bin/sh
# Idempotently create the seven control-room profiles and install skills/policies.
# Usage: scripts/profiles.sh [repo_root]
set -eu

REPO_ROOT="${1:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"
ROLES="orchestrator product-strategist architect builder quality-guardian self-improver"

log() { printf '%s\n' "[profiles] $*"; }

profile_home() {
  if hermes profile path "$1" >/dev/null 2>&1; then
    hermes profile path "$1"
  else
    printf '%s\n' "$HOME/.hermes/profiles/$1"
  fi
}

for role in $ROLES; do
  name="hermes-$role"
  if hermes profile list 2>/dev/null | grep -qx "$name"; then
    log "exists: $name"
  else
    hermes profile create "$name" >/dev/null
    log "created: $name"
  fi

  home="$(profile_home "$name")"
  skill_src="$REPO_ROOT/profiles/$role/skill.md"
  skill_dst="$home/skills/hermes-bootstraper/$role"
  mkdir -p "$skill_dst" "$home/skills/hermes-bootstraper/references"

  [ -f "$skill_src" ] || { log "MISSING skill source: $skill_src"; exit 1; }
  cp "$skill_src" "$skill_dst/SKILL.md"

  for policy in workflows safety-gates context-policy; do
    cp "$REPO_ROOT/shared/$policy.md" "$home/skills/hermes-bootstraper/references/$policy.md"
  done
  log "installed skill + policies: $name"
done

log "done"
