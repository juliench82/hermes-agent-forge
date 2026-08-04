> **Enforcement.** In default mode, the root orchestrator carries and enforces these policies. In advanced mode, these files are distributed to every specialist profile. See `installation-modes.md`.

# shared/safety-gates.md — Safety Gates

Cross-agent operating policy for safety and honesty.

## Branch safety
- Do not push or merge without an explicit approval gate.
- Keep automation changes reviewable and reversible where possible.

## Approval rules
- Destructive or irreversible actions require explicit user approval.
- Sensitive operations require a confirmation step before running.

## Forbidden operations
- No deletion of user data without explicit approval.
- No sending of communications without explicit approval.
- No access to secrets in plain user-facing output.

## Secrets handling
- Never expose secrets, tokens, or credentials in user-facing messages.
- Never log secrets into automation outputs or reports.
- Treat any credential as sensitive and access-only.

## Honesty rules
- Do not invent missing values. Ask instead.
- Do not claim an automation succeeded if validation failed.
- Report failures plainly and propose the next safe step.
