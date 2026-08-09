#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failures=0
check() {
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then
    printf 'PASS  %s\n' "$label"
  else
    printf 'FAIL  %s\n' "$label"
    failures=$((failures + 1))
  fi
}

printf 'Hermes bootstrapper doctor\nRoot: %s\n\n' "$ROOT_DIR"
check 'repository root exists' test -d "$ROOT_DIR"
check 'shared policies exist' test -f "$ROOT_DIR/shared/context-policy.md"
check 'safety enforcement exists' test -f "$ROOT_DIR/shared/safety-enforcement.md"
check 'profile contract exists' test -f "$ROOT_DIR/shared/profile-contract.md"
check 'skill contract exists' test -f "$ROOT_DIR/shared/skill-contract.md"
check 'task coordination contract exists' test -f "$ROOT_DIR/shared/task-coordination.md"
check 'handoff template exists' test -f "$ROOT_DIR/shared/handoff-template.md"
check 'self-improvement policy exists' test -f "$ROOT_DIR/shared/self-improvement-policy.md"
check 'profile directories exist' test -d "$ROOT_DIR/profiles"
check 'onboarding profile template exists' test -f "$ROOT_DIR/onboarding/templates/profile.yaml"
check 'git is available' command -v git
check 'hermes is available' command -v hermes

printf '\n'
if [ "$failures" -eq 0 ]; then
  printf 'Doctor result: PASS\n'
else
  printf 'Doctor result: FAIL (%s checks)\n' "$failures"
fi
exit "$failures"
