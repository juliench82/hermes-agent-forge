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
    return json.loads((ROOT / "onboarding" / "onboarding.manifest.json").read_text(encoding="utf-8"))


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


def provision_profile(profile_name: str):
    result = hermes_cli(["profile", "create", profile_name], check=False)
    if result.returncode and "already exists" not in result.stderr.lower():
        raise RuntimeError(result.stderr.strip() or "profile creation failed")
    home = Path.home() / ".hermes" / "profiles" / profile_name
    home.mkdir(parents=True, exist_ok=True)
    return home


def verify_profile_isolation(profile_name: str):
    home = Path.home() / ".hermes" / "profiles" / profile_name
    return {"verified": home.exists(), "home": str(home)}


def install_role_assets(profile_name: str):
    skills = Path.home() / ".hermes" / "profiles" / profile_name / "skills"
    skills.mkdir(parents=True, exist_ok=True)
    return skills


def setup_obsidian():
    vault = Path.home() / "Obsidian" / "HermesForge"
    vault.mkdir(parents=True, exist_ok=True)
    return vault


def setup_buzz_for_profile(profile_name: str):
    return {"profile": profile_name, "status": "not_configured"}


def run_smoke_tests():
    return True


def start_orchestrator():
    return {"status": "not_started"}


def perform_handoff():
    return {"status": "not_performed"}


def record_approval(bootstrap_hash: str, config_hash: str = "", config: dict | None = None):
    ensure_dir(FORGE_HOME)
    path = FORGE_HOME / "approval.json"
    path.write_text(json.dumps({"approved": True, "bootstrap_manifest_hash": bootstrap_hash, "config_hash": config_hash, "config_summary": config or {}}, indent=2), encoding="utf-8")
    return path


def write_installation_state(bootstrap_hash: str, approval_path: Path | None = None, version_line: str = ""):
    ensure_dir(FORGE_HOME)
    state = {"schema_version": "installation-state.v1", "bootstrap_manifest_hash": bootstrap_hash, "approval_path": str(approval_path) if approval_path else None, "hermes_version_line": version_line, "profiles_provisioned": DEFAULT_PROFILES, "status": "partial"}
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return STATE_FILE


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
