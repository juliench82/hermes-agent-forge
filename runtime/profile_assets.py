"""Safe repository-role asset provisioning for Hermes profile homes."""
from __future__ import annotations
import shutil
from pathlib import Path

ASSET_NAMES = ("SOUL.md", "skills")


def provision_profile_assets(repo_root: Path, profile: str, profile_home: Path) -> dict:
    source = repo_root / "profiles" / profile
    actions = []
    if not source.is_dir():
        return {"profile": profile, "status": "missing_source", "actions": actions, "verified": False}
    profile_home.mkdir(parents=True, exist_ok=True)
    for name in ASSET_NAMES:
        source_path = source / name
        target_path = profile_home / name
        if not source_path.exists():
            actions.append({"asset": name, "action": "missing_source"})
            continue
        if target_path.exists():
            actions.append({"asset": name, "action": "preserved", "path": str(target_path)})
            continue
        if source_path.is_dir():
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)
        actions.append({"asset": name, "action": "copied", "path": str(target_path)})
    verified = all((profile_home / name).exists() for name in ASSET_NAMES if (source / name).exists())
    return {"profile": profile, "status": "completed" if verified else "partial", "actions": actions, "verified": verified}


def provision_selected_profiles(repo_root: Path, profiles: list[str], homes_root: Path) -> list[dict]:
    return [provision_profile_assets(repo_root, name, homes_root / name) for name in profiles]
