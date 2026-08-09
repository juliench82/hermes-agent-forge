# Upgrade and Rollback

## Release identity

Every deployed Control Room has an immutable release identifier containing the repository revision, profile/policy bundle version, and provider configuration version.

## Upgrade sequence

1. Validate target release compatibility with the tenant manifest.
2. Confirm backups or provider rollback capability.
3. Record the current known-good release.
4. Apply the target release in a controlled deployment.
5. Run profile, transport, memory, connector, schedule, and smoke health checks.
6. Mark the release active only after all required checks pass.
7. Emit an audit event and notify the operator/customer of the result.

## Rollback triggers

Rollback or safe suspension is required when:

- A required profile cannot start or communicate.
- BUZZ or the memory layer fails its health check.
- A connector scope changes unexpectedly.
- Approval gates are bypassed or produce an invalid state.
- Acceptance or smoke tests fail.
- Error rates or resource usage exceed the tenant policy.

## Rollback rules

- Roll back to the last known-good release, not to an arbitrary mutable branch.
- Preserve audit records and diagnostics.
- Do not silently restore or broaden credentials.
- Keep external actions suspended until health and approval checks pass.
- If rollback cannot restore a safe state, suspend the tenant and escalate.
