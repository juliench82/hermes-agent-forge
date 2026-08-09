# Tenant Manifest

The tenant manifest is the provider-neutral description of one customer runtime. It contains references and policy, never credentials or customer data.

## Required identity

- `tenant_id`: stable, opaque identifier
- `display_name`: human-readable name
- `control_room_release`: version of this repository/runtime
- `owner`: approved customer/operator contact
- `timezone`: IANA timezone

## Runtime requirements

- `runtime_provider`: `hermes_cloud` | `self_hosted`
- `orchestrator_profile`: default user-facing profile
- `specialist_profiles`: native profiles participating in the control room
- `message_transport`: BUZZ or an approved equivalent
- `memory_layer`: customer-scoped Obsidian or approved alternative
- `schedules`: customer-scoped schedules and timezone

## Security references

- `secret_store_ref`: reference to the external secret manager; never a secret value
- `integration_register_ref`: approved connector scopes
- `approval_policy_ref`: customer approval policy
- `data_boundary_ref`: customer data and retention policy

## Lifecycle settings

- `desired_state`: `PROVISIONED` | `ACTIVE` | `SUSPENDED` | `DESTROYED`
- `backup_policy`: reference to approved backup policy
- `retention_policy`: reference to customer data lifecycle policy
- `healthcheck_interval`: expected healthcheck cadence

## Invariants

- A tenant has one isolated customer state boundary.
- Profiles receive only the credentials and context required for their assigned role.
- The manifest is safe to commit because it contains references, not secrets.
- A runtime provider must reject an incomplete or invalid manifest before provisioning.
