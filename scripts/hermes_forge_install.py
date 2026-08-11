#!/usr/bin/env python3
"""Compatibility API and entrypoint for the Hermes-native installer."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_PROFILES = ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"]
FORGE_HOME = Path.home() / ".hermes-forge"
STATE_FILE = FORGE_HOME / "installation_state.json"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_bootstrap_manifest():
    path = ROOT / "bootstrap.manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    required = ("schema_version", "repo_kind", "default_team", "installer_entrypoint", "installer_command")
    missing = [field for field in required if field not in manifest]
    if missing:
        raise ValueError(f"Missing required manifest fields: {', '.join(missing)}")
    if manifest["repo_kind"] != "bootstrap":
        raise ValueError("repo_kind must be bootstrap")
    return manifest, path


def load_onboarding_manifest():
    path = ROOT / "onboarding" / "onboarding.manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def hermes_cli(cmd, check=True):
    return subprocess.run(["hermes", *cmd], capture_output=True, text=True, check=check)


def hermes_json(cmd):
    result = hermes_cli([*cmd, "--json"], check=False)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def generate_config_yaml(profile_name: str, provider_config: dict):
    from runtime.adaptive_installer import config_yaml
    path = Path.home() / ".hermes" / "profiles" / profile_name / "config.yaml"
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(config_yaml(provider_config.get("provider", "nous"), provider_config.get("model", "default"), profile_name), encoding="utf-8")
    return path


def run_onboarding_wizard():
    from runtime.adaptive_installer import ask
    use_case = ask("Use case", "software project")
    role = ask("Your role", "founder/developer")
    default_size = 3 if any(x in use_case.lower() for x in ("solo", "content")) else 7 if "enterprise" in use_case.lower() else 5
    team_size = int(ask("Team size (3, 5, or 7)", str(default_size)))
    if team_size not in (3, 5, 7):
        raise ValueError("Team size must be 3, 5, or 7")
    return {"use_case": use_case, "role": role, "team_size": team_size, "provider": ask("Model provider", "nous"), "model": ask("Model", "default")}


def main():
    from runtime.adaptive_installer import main as installer_main
    return installer_main()


if __name__ == "__main__":
    raise SystemExit(main())
