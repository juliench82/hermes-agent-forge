# Release Readiness

## Status

The deterministic bootstrap implementation is complete through the merged roadmap PRs:

- PR #44: bootstrap-controller architecture documentation.
- PR #45: fixed bootstrap-controller contract.
- PR #46: main-profile asset preparation.
- PR #47: evidence-based skill verification.
- PR #48: transactional installation ledger and administrator escalation.
- PR #49: opt-in live Hermes acceptance contract.

Ordinary CI is deterministic. No live Hermes provisioning or Buzz runtime validation is claimed unless the opt-in acceptance procedure below has been run and its evidence reviewed.

## Live acceptance

Live acceptance is explicitly opt-in:

```bash
HERMES_LIVE_TESTS=1 HERMES_LIVE_HOME=/absolute/isolated/path python -m unittest discover
```

Before claiming completion, record evidence for:

- the installed Hermes version and supported CLI help;
- the isolated Hermes home/profile root used for the run;
- main-profile SOUL.md and config.yaml creation or preservation;
- observed bootstrap skill identities and post-install listings;
- dynamic customer-team discovery and exact approved plan hash;
- profile, skill, and asset verification results;
- rerun/idempotency behavior;
- failure recovery, bounded repair, and administrator escalation.

Do not run this suite against a production Hermes home. Do not place credentials in plans, prompts, logs, or repository files.

## Buzz boundaries

The official Hermes Buzz integration describes three distinct modes:

1. Buzz Desktop manages a local Hermes process.
2. `buzz-acp` bridges a Buzz channel to Hermes ACP over stdio.
3. The native gateway uses NIP-42-authenticated Nostr WebSocket transport with CLI fallback.

These modes are not interchangeable. Native gateway validation must additionally verify dedicated identity/keypair handling, relay and public-key locking, channel/DM routing, approval delivery, and reconnect behavior. Desktop and ACP validation must verify their own process ownership and access boundaries.

No Buzz mode is considered live-validated by deterministic repository tests alone.

## Administrator recovery

The installation ledger is the source of truth for recovery. Required operation records cover profile, skill, and asset targets and must contain verified evidence before completion.

Expected states include:

- `planned`
- `approved`
- `provisioning`
- `verifying`
- `repairing`
- `completed`
- `partial`
- `admin_action_required`
- `failed`

When bounded repair is exhausted, the controller must persist the ledger, transition to `admin_action_required`, notify the configured administrator adapter when available, and avoid further provisioning. Resume only after reviewing the persisted plan hash, operation results, diagnostics, and remediation decision.

## Security checklist

- Keep customer team discovery dynamic; do not add domain-to-profile mappings.
- Require exact observed skill identities; never install guessed slugs.
- Use list-argument subprocess calls and bounded timeouts.
- Preserve existing profile assets unless replacement is explicit.
- Keep live tests opt-in and isolated.
- Scan repository changes with the available secret-scanning mechanism.
- Treat unavailable secret scanning or unrun live acceptance as an explicit release limitation, not a passing result.
