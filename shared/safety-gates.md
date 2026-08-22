# Safety Gates

This document defines the safety gates that must pass before any runtime operation proceeds.

## Alignment with Hermes Security Model

Safety gates implement Hermes's 8-layer security model at the runtime level.

See: https://hermes-agent.nousresearch.com/docs/user-guide/security

## Gate Definitions

1. **User Authorization** — Platform OAuth validation
2. **Command Approval** — Hermes `approvals:` config + hardline blocklist
3. **Write Boundaries** — `HERMES_WRITE_SAFE_ROOT` enforcement
4. **Container Check** — Docker backend availability
5. **Credential Redaction** — MCP response filtering
6. **Context Scan** — Prompt injection scanner (automatic)
7. **Profile Isolation** — Profile home directory boundaries
8. **Input Validation** — Length limits, sanitization (automatic)

## Testing

All gates are tested in:
- `tests/test_runtime_enforcement.py`
- `tests/test_approval.py`
- `tests/test_installer_hardening.py`

## Related Docs

- `shared/safety-enforcement.md` — Enforcement policy overview
- `shared/context-policy.md` — Context file handling
