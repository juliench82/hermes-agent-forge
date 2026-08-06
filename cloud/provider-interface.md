# Provider Interface

The Control Room is portable because deployment concerns sit behind a provider adapter. This is a contract, not a claim that every provider already implements it.

## Operations

```text
validate(manifest) -> validation_result
provision(manifest) -> tenant_runtime
deploy(tenant_runtime, release) -> deployment_result
status(tenant_id) -> tenant_status
suspend(tenant_id, reason) -> operation_result
resume(tenant_id) -> operation_result
upgrade(tenant_id, release) -> deployment_result
rollback(tenant_id, release) -> deployment_result
rotate_secret(tenant_id, secret_ref) -> operation_result
destroy(tenant_id, retention_policy) -> operation_result
```

## Required behaviour

- Every mutating operation accepts an idempotency key.
- Every operation is scoped by an opaque `tenant_id`.
- Provider errors are returned with a safe diagnostic; secrets and tokens are redacted.
- Operations emit audit events with tenant, release, operation, actor, status, and timestamp.
- Providers must support a kill switch for action-capable workflows.
- Providers must expose enough status for the orchestrator/operator to distinguish healthy, degraded, suspended, and failed states.

## Adapter targets

### Hermes Cloud

Use when the platform provides the required tenant lifecycle, profile/runtime configuration, storage, schedules, credential isolation, and commercial permissions. Hermes Cloud is a candidate adapter, not a hard dependency.

### Self-hosted

Use a customer or operator-managed VPS, container platform, or dedicated environment. The adapter owns provisioning, updates, networking, backups, secrets, and observability.

## Boundary

The public repository defines this contract. A private management service may implement adapters, billing, customer identity, OAuth callbacks, secret storage, support tooling, and tenant registry outside this repository.
