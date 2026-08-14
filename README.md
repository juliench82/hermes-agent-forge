# Hermes Agents Forge

Hermes Agents Forge is a Hermes-native bootstrap repository. It does not install a preselected business team or predict a customer’s domain. Instead, the fresh Hermes default profile prepares the Hermes environment, then Hermes discovers the customer-specific team from free-text goals.

## The key idea

There are two different kinds of profiles:

1. **Bootstrap controller** — the fresh Hermes default/main profile. This is the platform control plane that reads this repository, prepares and verifies its own assets, runs onboarding, supervises provisioning, and escalates unresolved failures to the human administrator.
2. **Customer team** — profiles designed dynamically by Hermes after onboarding. Names, roles, descriptions, capabilities, and skills are generated from the customer’s objective and are never selected from a repository-side domain catalog.

## Release readiness

The deterministic implementation phases are complete through PR #49. See [`RELEASE_READINESS.md`](RELEASE_READINESS.md) for the live-acceptance evidence checklist, administrator recovery procedure, Buzz integration boundaries, and explicit release limitations.

Live Hermes and Buzz validation remain opt-in and are not claimed by ordinary CI.
