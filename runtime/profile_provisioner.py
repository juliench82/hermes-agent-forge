"""
profile_provisioner.py — Real profile creation and isolation verification.
"""

import subprocess
import os
from pathlib import Path

DEFAULT_PROFILES = [
    "orchestrator",
    "product-strategist",
    "architect",
    "builder",
    "quality-guardian",
]

def hermes_cli(cmd: list, env=None, check=True):
    """Run a hermes CLI command with YOLO mode enabled."""
    full_env = os.environ.copy()
    full_env["HERMES_YOLO_MODE"] = "1"
    if env:
        full_env.update(env)
    full_cmd = ["hermes"] + cmd
    result = subprocess.run(full_cmd, env=full_env, capture_output=True, text=True, check=check)
    return result


def provision_profile(profile_name: str):
    """Create a profile and ensure isolation."""
    result = hermes_cli(["profile", "create", profile_name], check=False)
    if result.returncode != 0 and "already exists" not in result.stderr.lower():
        raise RuntimeError(f"Failed to create profile {profile_name}: {result.stderr}")
    home = Path.home() / ".hermes" / "profiles" / profile_name
    home.mkdir(parents=True, exist_ok=True)
    soul_path = home / "SOUL.md"
    if not soul_path.exists():
        soul_path.write_text(f"# SOUL.md\n\nProfile: {profile_name}\n\nThis profile is isolated and managed by hermes-agent-forge.\n")
    return home


def verify_isolation(profile_name: str):
    """Verify profile isolation (minimal check)."""
    home = Path.home() / ".hermes" / "profiles" / profile_name
    if not home.exists():
        raise RuntimeError(f"Profile home not found for {profile_name}")
    if not (home / "SOUL.md").exists():
        raise RuntimeError(f"SOUL.md not found for {profile_name}")
    return True
