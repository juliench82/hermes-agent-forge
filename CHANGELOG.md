# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `LICENSE` (MIT), `.gitignore`, `pyproject.toml` for proper Python packaging
- `AGENTS.md` for cross-tool agent instructions
- `CONTRIBUTING.md` and `CHANGELOG.md` for contributor guidance
- `Dockerfile` for isolated runtime testing
- `site/public/.well-known/skills/index.json` for skill discovery

### Changed
- `catalog/connectors/` primitives aligned with Hermes MCP server definitions
- `catalog/triggers/cron/` aligned with native `cronjob` tool
- `shared/safety-*.md` docs reference Hermes 8-layer security model
- `onboarding/` docs include `hermes skills trust` and `hermes setup --portal` steps
- `HERMES.md` updated with skills trust guidance

### Removed
- `site/index_new.html`, `site/script_new.js`, `site/styles_new.css` (stale duplicates)

### Fixed
- `site/public/install.sh` synced with root `install.sh`
- `site/public/llms.txt` synced with `site/llms.txt`

## [0.1.0] — 2026-08-22

### Added
- Initial release of Hermes Agents Forge
- Bootstrap manifest system for multi-profile team provisioning
- Compiler for discovering and activating bootstrap manifests
- Runtime for profile provisioning, skill resolution, and policy enforcement
- Catalog of versioned primitives (roles, connectors, triggers, memory, policies)
- Onboarding system with templates, workflows, and fixtures
- Skills/forge SKILL.md for agent capabilities
- Website with llms.txt for LLM discoverability
- CI/CD workflows for validation
- Comprehensive test suite (43 test files)

[Unreleased]: https://github.com/juliench82/hermes-agents-forge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/juliench82/hermes-agents-forge/releases/tag/v0.1.0
