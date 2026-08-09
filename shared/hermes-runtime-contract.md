# Hermes Runtime Contract v1 (Draft)

**Status**: `draft`
**Contract Version**: `v1-draft`
**Compatibility**: `solo-founder profiles`

## Purpose

Defines the runtime contract between the Hermes bootstrapper compiler and the Hermes kernel/runtime.

## Contract Status

This is a **draft** contract. The `compiler/hermes_adapter.py` emits bundles marked with `contractStatus: compatibility`.

## Bundle Structure

```json
{
  "contract_version": "v1-draft",
  "contract_status": "compatibility",
  "fingerprint": "<sha256>",
  "runtime": {},
  "coordination": {},
  "manifest": {}
}
```

## Security Invariants

1. Secret references only (no values)
2. Per-agent isolation
3. Default-deny egress
4. Least privilege (allowlist)
5. Confirmation for irreversible actions
6. Acyclic delegation
7. Append-only audit logging

## References

- `shared/profile-contract.md`
- `shared/task-coordination.md`
- `shared/safety-enforcement.md`
- `runtime/hermes_kernel.py`
- `compiler/hermes_adapter.py`
