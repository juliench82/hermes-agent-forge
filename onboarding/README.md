# Onboarding Guide

This guide walks you through the complete onboarding flow.

## Pre-Onboarding Checklist

- [ ] Hermes installed
- [ ] Model configured (`hermes setup --portal`)
- [ ] Skills trusted (`hermes skills trust`)
- [ ] Python 3.11+ available
- [ ] Dependencies installed

## Onboarding Workflows

1. **Activation Review** — Verify bootstrap activated correctly
2. **Connector Authorization** — Authorize MCP servers
3. **Vault Path** — Set up secrets management

See `onboarding/workflows/` for detailed specs.

## Onboarding Templates

Templates in `onboarding/templates/` generate profile assets.

## Post-Onboarding

1. Test profiles: `hermes profile list`
2. Explore skills: `hermes skills list`
3. Review security: `shared/safety-enforcement.md`

## Troubleshooting

- **Onboarding fails**: Check Hermes version (2026.8.x+)
- **Skills not loading**: Run `hermes skills trust`
- **MCP not connecting**: Check credentials in `~/.hermes/.env`

## Related Docs

- `onboarding/START.md` — Quick start
- `onboarding/manifest.md` — Manifest spec
- `tests/test_onboarding.py` — Tests
