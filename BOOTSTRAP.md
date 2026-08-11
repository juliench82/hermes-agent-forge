# Bootstrap — hermes-agent-forge

This repository is a **bootstrap repository** for Hermes Agent. It is **not** your application repository.

## Getting started (CLI-first)

**Important:** This installer is designed for **Hermes CLI** (terminal), not Desktop/browser. The bootstrap repo is read-only during discovery/setup.

### Step 1: Clone the repo

```bash
git clone https://github.com/juliench82/hermes-agent-forge.git
cd hermes-agent-forge
```

### Step 2: Enable YOLO mode

In your Hermes CLI or Desktop session, run:

```
/yolo
```

This enables auto-approval for the current session.

### Step 3: Run the installer

```bash
python3 scripts/hermes_forge_install.py
```

The installer will:

- Read `bootstrap.manifest.json` and `onboarding/onboarding.manifest.json` (read-only).
- Run an adaptive onboarding wizard to collect your provider/model/config choices.
- Provision 5 isolated profiles: `orchestrator`, `product-strategist`, `architect`, `builder`, `quality-guardian`.
- Generate per-profile `config.yaml` templates.
- Optionally provision main-profile `SOUL.md` (Forge bootstrap coordinator personality).
- Write installation state, audit logs, and approval records to `~/.hermes-forge/` (outside the cloned repo).
- Report truthful status (`completed` or `partial`).

## Configuration onboarding

The installer will prompt you for:

1. **Provider selection**
   - Nous Portal (OAuth — recommended)
   - API-key provider (Nvidia, OpenAI, etc.)
   - Custom OpenAI-compatible endpoint
   - Skip (configure manually later)

2. **Model policy**
   - One shared model for all profiles (default)
   - Override per role (advanced)

3. **Operational preferences**
   - Obsidian vault: create Forge vault / skip
   - BUZZ: configure now / skip
   - Gateway: start after smoke tests / provision only

4. **Explicit approval**
   - Review configuration summary
   - Approve (bound to bootstrap manifest hash + config hash)

## Security

- No credentials, API keys, or secrets are stored in this repository.
- Secrets are managed by Hermes in `.env` files under `~/.hermes/profiles/<name>/`.
- Installation state and audit logs are written to `~/.hermes-forge/` (outside the cloned repo).

## For developers

- Installer entrypoint: `scripts/hermes_forge_install.py`
- Runtime modules: `runtime/`
- Tests: `tests/e2e_clean_install/`
- State directory: `~/.hermes-forge/`
