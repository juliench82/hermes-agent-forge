#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
STATE_DIR="${HOME}/.hermes-forge"
mkdir -p "$STATE_DIR"
if ! command -v hermes >/dev/null 2>&1; then
  printf '%s\n' '{"schema_version":"installation-state.v1","status":"partial","error":"Hermes CLI is unavailable"}' > "$STATE_DIR/installation_state.json"
  printf '%s\n' 'Hermes CLI is unavailable; installation stopped.' >&2
  exit 1
fi
if ! hermes chat --command "/yolo" >/dev/null 2>&1; then
  printf '%s\n' '{"schema_version":"installation-state.v1","status":"partial","error":"Hermes YOLO activation failed"}' > "$STATE_DIR/installation_state.json"
  printf '%s\n' 'Hermes YOLO activation failed; installation stopped.' >&2
  exit 1
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$ROOT/scripts/hermes_forge_install.py" "$@"
fi
if command -v python >/dev/null 2>&1; then
  exec python "$ROOT/scripts/hermes_forge_install.py" "$@"
fi
printf '%s\n' '{"schema_version":"installation-state.v1","status":"partial","error":"Python runtime unavailable after native Hermes activation"}' > "$STATE_DIR/installation_state.json"
printf '%s\n' 'Python runtime unavailable; native activation succeeded but provisioning did not run.' >&2
exit 1
