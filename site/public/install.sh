#!/usr/bin/env sh
# Hermes Agents Forge — compatibility installer.
#
# The canonical install path is:
#     hermes skills install https://hermes-agents-forge.vercel.app/SKILL.md
#
# This wrapper exists only for environments where a script is expected. It:
#   - requires no sudo and never escalates privileges,
#   - verifies that `hermes` exists on PATH,
#   - downloads the pinned, versioned SKILL.md and verifies its sha256 when a
#     checksum is pinned at release time,
#   - never pipes remote content into a shell,
#   - prints the next step when done.
set -eu

FORGE_DOMAIN="hermes-agents-forge.vercel.app"
FORGE_VERSION="0.1.0"        # pinned artifact version
SKILL_URL="https://${FORGE_DOMAIN}/SKILL.md"
PINNED_SHA256=""             # set at release time; see site/README.md checklist

info() { printf '%s\n' "$*"; }
fail() { printf 'error: %s\n' "$*" >&2; exit 1; }

command -v hermes >/dev/null 2>&1 \
  || fail "hermes not found on PATH. Install Hermes first, then re-run."

if [ -n "$PINNED_SHA256" ]; then
  command -v curl >/dev/null 2>&1 || fail "curl is required to fetch $SKILL_URL"
  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT
  curl -fsSL "$SKILL_URL" -o "$tmp" || fail "download failed: $SKILL_URL"
  if command -v sha256sum >/dev/null 2>&1; then
    actual="$(sha256sum "$tmp" | awk '{print $1}')"
  else
    actual="$(shasum -a 256 "$tmp" | awk '{print $1}')"
  fi
  [ "$actual" = "$PINNED_SHA256" ] \
    || fail "checksum mismatch for SKILL.md v${FORGE_VERSION} (expected $PINNED_SHA256, got $actual)"
  # Install the verified copy into the user-space skills library.
  skill_dir="${HERMES_HOME:-$HOME/.hermes}/skills/forge"
  mkdir -p "$skill_dir"
  cp "$tmp" "$skill_dir/SKILL.md"
  info "Forge v${FORGE_VERSION} installed to $skill_dir (checksum verified)."
else
  info "note: no pinned checksum configured for this release; delegating to hermes."
  hermes skills install "$SKILL_URL" || fail "hermes skills install failed"
fi

info ""
info "Next step: open Hermes and type /forge"
