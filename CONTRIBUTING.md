# Contributing to Hermes Agents Forge

Thanks for contributing! This doc covers the essentials.

## Quick Start

1. **Fork** the repo and clone locally
2. **Create a branch** using the naming convention: `<type>/<short-description>` (e.g., `feat/dynamic-profiles`, `fix/connector-mcp`, `docs/update-onboarding`)
3. **Make your changes** and ensure tests pass
4. **Open a PR** with a clear title and description

## Branch Naming

- `feat/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `chore/` — Cleanup, refactors, tooling
- `test/` — Test additions or improvements

## Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check .
black --check .
```

## Code Style

- **Python**: Follow PEP 8, use type hints, max line length 100
- **YAML**: 2-space indentation, consistent key ordering
- **Markdown**: Sentence case headers, proper code fencing

## PR Guidelines

- **One logical change per PR** — split large refactors into multiple PRs
- **Include tests** for new functionality
- **Update docs** if behavior changes
- **Reference issues** where applicable (e.g., "Closes #42")

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(compiler): add bootstrap discovery with manifest validation
fix(runtime): handle missing profile assets gracefully
docs(README): clarify onboarding flow
chore(deps): bump pyyaml to 6.0.1
```

## Release Process

Releases are cut manually. To propose a release:

1. Update `CHANGELOG.md` with your changes
2. Bump version in `pyproject.toml`
3. Tag the release commit (e.g., `v0.1.0`)
4. Create a GitHub release with the changelog entry

## Questions?

Open an issue or tag @juliench82 in a discussion.
