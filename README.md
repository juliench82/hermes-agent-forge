# Hermes Agents Forge

Open this repository in Hermes and start the agent in this folder. Hermes must immediately ask: **What do you want to accomplish with Hermes?** It must not summarize the architecture or offer a code tour.

Hermes Agents Forge is a Hermes-native bootstrap repository. It does not install a preselected business team. The fresh Hermes default/main profile is the bootstrap controller. Customer teams are discovered dynamically from free-text goals.

## The key idea

There are two different kinds of profiles:

1. **Bootstrap controller** — the fresh Hermes default/main profile. It reads this repository, prepares itself, runs onboarding, supervises provisioning, and escalates unresolved failures.
2. **Customer team** — profiles designed dynamically after onboarding. Names, roles, capabilities, and skills come from the customer's objective, never from a repository-side domain catalog.

Do not treat `profiles/` as the customer team. Do not run `install.sh` as the normal customer path.

## Release readiness

The deterministic implementation phases are complete through PR #49. See [`RELEASE_READINESS.md`](RELEASE_READINESS.md) for live-acceptance evidence, administrator recovery, Buzz boundaries, and explicit limitations.

Live Hermes and Buzz validation remain opt-in and are not claimed by ordinary CI.
