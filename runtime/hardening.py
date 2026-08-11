"""Small, dependency-free hardening primitives for the adaptive installer."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

MANAGED_BEGIN = "# BEGIN HERMES-FORGE MANAGED CONFIG\n"
MANAGED_END = "# END HERMES-FORGE MANAGED CONFIG\n"


def managed_config(existing: str, generated: str) -> tuple[str, str]:
    """Replace only the Forge-managed block and preserve all user-owned text."""
    block = MANAGED_BEGIN + generated.rstrip() + "\n" + MANAGED_END
    start, end = existing.find(MANAGED_BEGIN), existing.find(MANAGED_END)
    if start >= 0 and end >= start:
        end += len(MANAGED_END)
        return existing[:start] + block + existing[end:], "updated"
    if existing:
        separator = "" if existing.endswith("\n") else "\n"
        return existing + separator + "\n" + block, "appended"
    return block, "generated"


def write_managed_config(path: Path, generated: str) -> str:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    content, action = managed_config(current, generated)
    if content != current:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return action


def verify_profile(home: Path) -> dict:
    checks = {"home": home.exists(), "config": (home / "config.yaml").is_file(), "soul": (home / "SOUL.md").is_file()}
    return {"verified": all(checks.values()), "checks": checks, "home": str(home)}


def write_truthful_state(path: Path, config: dict, profiles: list[dict], errors: list[dict]) -> str:
    status = "completed" if not errors and profiles and all(item.get("verified") for item in profiles) else "partial"
    state = {"schema_version": "installation-state.v1", "status": status, "config_summary": {"provider": config.get("provider"), "model": config.get("model"), "team_size": config.get("team_size")}, "profiles_provisioned": profiles, "errors": errors, "updated_at": datetime.now(timezone.utc).isoformat()}
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temporary.replace(path)
    return status
