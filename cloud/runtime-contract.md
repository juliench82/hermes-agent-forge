# Runtime Contract

This contract defines what any deployment backend must provide to run the Hermes Control Room. The implementation may be Hermes Cloud, self-hosted infrastructure, or a future provider.

## Provision

Create the tenant boundary, native profiles, customer-scoped storage, message transport configuration, schedules, secret references, and health checks from a validated tenant manifest.

Provisioning must be idempotent. A repeated request must reconcile the desired state rather than create duplicate profiles, schedules, or credentials.

## Deploy

Install a specific Control Room release and apply the tenant blueprint, policies, profile configuration, approved integrations, and runtime settings. The provider must return a release identifier and deployment status.

## Run

Expose the orchestrator as the only normal customer-facing entry point. Route specialist handoffs through the configured transport, keep customer state tenant-scoped, execute schedules in the tenant timezone, and emit operational events.

## Suspend

Stop scheduled and action-capable execution while preserving enough state for diagnosis and safe resume. Suspension must not delete customer data, credentials, or audit records.

## Resume

Re-enable only the previously approved release, schedules, connector scopes, and approval policy. A changed scope requires a new activation review.

## Upgrade

Validate the target release against the tenant manifest, create a rollback point, apply the release, run health checks, and report the result. Failed upgrades must restore the last known-good release or leave the tenant safely suspended.

## Destroy

Revoke connector access, stop execution, delete runtime resources, and process customer data according to the retention/deletion policy. Destruction must be explicit, auditable, and non-reversible after the retention window.

## Provider obligations

Every provider must document: idempotency, isolation boundary, secret handling, backup/restore, health checks, logs, costs/limits, failure modes, and deletion semantics.
