# Onboarding Quick Start

Welcome to Hermes Agents Forge!

## Prerequisites

- Python 3.11+
- Git
- Hermes Agent

## Step 1: Install Hermes

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

## Step 2: Fast Setup (Recommended)

```bash
hermes setup --portal
```

This covers model provider + Tool Gateway in one OAuth.

## Step 3: Clone and Trust Skills

```bash
git clone https://github.com/juliench82/hermes-agents-forge
cd hermes-agents-forge
hermes skills trust
```

**Why?** Hermes requires explicit trust for project-local skills.

## Step 4: Run the Bootstrap

```bash
pip install -e ".[dev]"
python -m compiler --manifest bootstrap.manifest.json
```

## Step 5: Follow Onboarding Workflows

See `onboarding/workflows/` for details.

## Troubleshooting

- **Skills not loaded**: Run `hermes skills trust`
- **Model not configured**: Run `hermes setup --portal`
- **MCP connection failed**: Check `~/.hermes/.env`

## Related Docs

- `onboarding/README.md` — Full guide
- `HERMES.md`, `AGENTS.md` — Context files
- `CONTRIBUTING.md` — How to contribute
