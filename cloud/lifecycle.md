# Tenant Lifecycle

## States

```text
REQUESTED → VALIDATED → PROVISIONING → PROVISIONED → DEPLOYING → ACTIVE
                              ↓              ↓           ↓
                           FAILED       DESTROYED   DEGRADED
                                                           ↓
                                                        SUSPENDED
```

## State meanings

- `REQUESTED`: a tenant manifest exists but has not passed validation.
- `VALIDATED`: required references, policies, scopes, and runtime capabilities are present.
- `PROVISIONING`: provider resources are being created or reconciled.
- `PROVISIONED`: the tenant boundary exists but the Control Room release is not active.
- `DEPLOYING`: a release is being installed and verified.
- `ACTIVE`: health checks pass and approved workflows may run.
- `DEGRADED`: the tenant remains present but one or more required capabilities are unhealthy.
- `SUSPENDED`: execution and schedules are paused by policy, failure, or operator action.
- `FAILED`: an operation failed; no action-capable workflow may run until recovered.
- `DESTROYED`: runtime resources have been removed and deletion/retention processing is complete.

## Transition rules

- Validation failure never enters `PROVISIONING`.
- Only a successful deployment and healthcheck may enter `ACTIVE`.
- `DEGRADED` or `FAILED` must fail closed for external actions.
- A customer or authorised operator may request `SUSPENDED` or `DESTROYED`.
- Resuming after a material configuration or scope change requires a new activation review.
- Every transition emits an audit event.
