# Safety Enforcement Policy

This document defines the safety enforcement boundaries for Hermes Agents Forge runtime operations.

## Alignment with Hermes 8-Layer Security Model

All security primitives in this project reference Hermes Agent's comprehensive 8-layer defense-in-depth model:

1. **User Authorization** — Platform-level auth (Telegram, Discord, Slack OAuth)
2. **Dangerous Command Approval** — Smart/manual/off modes with hardline blocklist
3. **File Write Safety** — `HERMES_WRITE_SAFE_ROOT` boundaries
4. **Container Isolation** — Docker backend for untrusted code execution
5. **MCP Credential Filtering** — Automatic redaction of secrets in tool responses
6. **Context File Scanning** — Prompt injection detection before loading
7. **Cross-Session Isolation** — Profile-level session boundaries
8. **Input Sanitization** — User input validation and length limits

See: https://hermes-agent.nousresearch.com/docs/user-guide/security

## Runtime Enforcement Points

### Command Approval (`runtime/approval.py`)

- Delegates to Hermes's native approval system via `approvals:` config
- Supports smart/manual/off modes
- Implements hardline blocklist for truly dangerous commands
- Allows user-defined deny rules via config

### File Write Safety (`runtime/hardening.py`)

- Respects `HERMES_WRITE_SAFE_ROOT` environment variable
- Requires explicit approval for writes outside safe root
- Logs all write operations to audit trail

### Isolation (`runtime/isolation.py`)

- Provisions profiles in isolated Hermes home directories
- Optional Docker backend for container isolation
- Enforces profile boundaries

### Secrets (`runtime/secrets.py`)

- Writes secrets to `~/.hermes/.env` (Hermes-native location)
- Non-secret settings to `~/.hermes/config.yaml`
- References Hermes's protected paths

## Related Docs

- `shared/safety-gates.md` — Safety gate definitions
- `shared/context-policy.md` — Context file handling
- `catalog/policies/mandatory-baseline/1.0.0/policy.yaml` — Baseline policy config
