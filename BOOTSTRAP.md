# Bootstrap — hermes-agent-forge

This repository is a **bootstrap repository** for Hermes Agent. It is **not** your application repository.

## Getting started (non-technical users)

1. Ensure Hermes Agent is installed on your machine.
2. In Hermes, point to this repository URL:
   ```
   https://github.com/juliench82/hermes-agent-forge
   ```
3. Hermes will read `bootstrap.manifest.json` and run the installer:
   ```
   scripts/hermes_forge_install.py
   ```
4. The installer will:
   - Enable **YOLO mode** for the install session (no repeated approval prompts).
   - Provision 5 profiles: `orchestrator`, `product-strategist`, `architect`, `builder`, `quality-guardian`.
   - Install role assets, Obsidian vault, BUZZ identities, and run smoke tests.
   - Start the orchestrator gateway and perform a handoff to product-strategist.
   - Report truthful persistent runtime status in `runtime/installation_state.json`.

## YOLO mode

This installer uses Hermes **YOLO mode** (`HERMES_YOLO_MODE=1`) to bypass approval prompts during installation. YOLO mode is documented in the Hermes docs and is equivalent to `approval_mode: off` in config.

## Manifests

- `bootstrap.manifest.json` — machine-readable bootstrap manifest (schema: `schemas/bootstrap-manifest.v1.schema.json`).
- `onboarding/onboarding.manifest.json` — adaptive business onboarding manifest.

## Security

- No credentials, API keys, or secrets are stored in this repository.
- All sensitive configuration is managed by Hermes in your local profile homes under `~/.hermes/profiles/`.

## For developers

- Installer entrypoint: `scripts/hermes_forge_install.py`
- Runtime modules: `runtime/`
- Tests: `tests/e2e_clean_install/`
