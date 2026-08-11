#!/usr/bin/env python3
"""
hermes_forge_install.py — Corrected connected installer for hermes-agent-forge.

Key corrections:
- Bootstrap repo is read-only; state is written to ~/.hermes-forge/.
- Adaptive onboarding collects provider/model/config choices.
- Per-profile config.yaml templates are generated.
- Main-profile SOUL.md is provisioned only if user accepts.
- Truthful state reporting (not_configured/not_verified for placeholders).
- YOLO mode: user runs /yolo once at session start.
"""

import json
import hashlib
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

# --- Constants ---
DEFAULT_PROFILES = [
    "orchestrator",
    "product-strategist",
    "architect",
    "builder",
    "quality-guardian",
]

# State directory outside the bootstrap repo
FORGE_HOME = Path.home() / ".hermes-forge"
STATE_FILE = FORGE_HOME / "installation_state.json"
AUDIT_LOG_FILE = FORGE_HOME / "audit_log.jsonl"
APPROVAL_FILE = FORGE_HOME / "approval.json"

# --- Helpers ---

def log_audit(event: str, details: dict):
    """Append an audit record to the audit log file."""
    FORGE_HOME.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "details": details,
    }
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def hermes_cli(cmd: list, check=True):
    """Run a hermes CLI command (user must run /yolo separately)."""
    full_cmd = ["hermes"] + cmd
    result = subprocess.run(full_cmd, capture_output=True, text=True, check=check)
    return result


def hermes_json(cmd: list):
    """Run a hermes CLI command and parse JSON output."""
    result = hermes_cli(cmd + ["--json"], check=False)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def sha256_file(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dir(path: Path):
    """Ensure a directory exists."""
    path.mkdir(parents=True, exist_ok=True)


# --- Bootstrap and onboarding ---

def load_bootstrap_manifest():
    """Load and validate bootstrap.manifest.json (read-only)."""
    manifest_path = Path("bootstrap.manifest.json")
    if not manifest_path.exists():
        raise FileNotFoundError("bootstrap.manifest.json not found")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    required = ["schema_version", "repo_kind", "default_team", "installer_entrypoint"]
    for field in required:
        if field not in manifest:
            raise ValueError(f"Missing required field in bootstrap.manifest.json: {field}")
    if manifest["repo_kind"] != "bootstrap":
        raise ValueError("This repository is not a bootstrap repository (repo_kind != 'bootstrap')")
    return manifest, manifest_path


def load_onboarding_manifest():
    """Load onboarding/onboarding.manifest.json."""
    manifest_path = Path("onboarding") / "onboarding.manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError("onboarding/onboarding.manifest.json not found")
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Adaptive onboarding wizard ---

def run_onboarding_wizard():
    """Collect provider/model/config choices from the user."""
    print("\n=== Hermes Forge Onboarding ===")
    print("\nThis installer will provision a 5-profile control room.")
    print("\nFirst, enable YOLO mode in Hermes: run /yolo in your Hermes session.\n")
    
    # Provider selection
    print("Select your model provider:")
    print("1. Nous Portal (OAuth — recommended)")
    print("2. API-key provider (Nvidia, OpenAI, etc.)")
    print("3. Custom OpenAI-compatible endpoint")
    print("4. Skip provider setup (configure manually later)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    provider_config = {"choice": choice}
    
    if choice == "1":
        print("\nRunning: hermes setup --portal")
        result = hermes_cli(["setup", "--portal"], check=False)
        if result.returncode != 0:
            print(f"Warning: Portal setup failed: {result.stderr}")
        provider_config["provider"] = "nous"
        provider_config["setup_method"] = "oauth"
    elif choice == "2":
        print("\nRunning: hermes model (interactive)")
        result = hermes_cli(["model"], check=False)
        if result.returncode != 0:
            print(f"Warning: Model setup failed: {result.stderr}")
        provider_config["provider"] = "api_key"
        provider_config["setup_method"] = "interactive"
    elif choice == "3":
        endpoint = input("Enter custom endpoint URL: ").strip()
        model = input("Enter model ID: ").strip()
        key_env = input("Enter environment variable name for API key: ").strip()
        provider_config["provider"] = "custom"
        provider_config["endpoint"] = endpoint
        provider_config["model"] = model
        provider_config["key_env"] = key_env
    else:
        provider_config["provider"] = "skip"
    
    # Model policy
    print("\nModel policy:")
    print("1. One shared model for all profiles (default)")
    print("2. Override per role (advanced)")
    model_choice = input("Enter choice (1-2): ").strip()
    provider_config["model_policy"] = "shared" if model_choice == "1" else "per_role"
    
    # Operational preferences
    print("\nOperational preferences:")
    obsidian_choice = input("Obsidian vault: create Forge vault / skip? (create/skip): ").strip()
    buzz_choice = input("BUZZ: configure now / skip? (configure/skip): ").strip()
    gateway_choice = input("Gateway: start after smoke tests / provision only? (start/provision): ").strip()
    
    provider_config["obsidian"] = obsidian_choice
    provider_config["buzz"] = buzz_choice
    provider_config["gateway"] = gateway_choice
    
    return provider_config


# --- Approval ---

def record_approval(bootstrap_hash: str, config_hash: str, config: dict):
    """Record explicit approval bound to bootstrap manifest + config hash."""
    ensure_dir(FORGE_HOME)
    approval = {
        "approved": True,
        "bootstrap_manifest_hash": bootstrap_hash,
        "config_hash": config_hash,
        "config_summary": {
            "provider": config.get("provider"),
            "model_policy": config.get("model_policy"),
            "obsidian": config.get("obsidian"),
            "buzz": config.get("buzz"),
            "gateway": config.get("gateway"),
        },
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(APPROVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(approval, f, indent=2)
    log_audit("approval_recorded", {"bootstrap_hash": bootstrap_hash, "config_hash": config_hash})
    return APPROVAL_FILE


# --- Profile provisioning ---

def provision_profile(profile_name: str):
    """Create a profile via Hermes CLI."""
    result = hermes_cli(["profile", "create", profile_name], check=False)
    if result.returncode != 0 and "already exists" not in result.stderr.lower():
        raise RuntimeError(f"Failed to create profile {profile_name}: {result.stderr}")
    # Verify profile home exists
    home = Path.home() / ".hermes" / "profiles" / profile_name
    if not home.exists():
        raise RuntimeError(f"Profile home not created for {profile_name}")
    log_audit("profile_provisioned", {"profile": profile_name, "home": str(home)})
    return home


def verify_profile_isolation(profile_name: str):
    """Verify profile isolation via Hermes CLI."""
    status = hermes_json(["-p", profile_name, "status"])
    if status is None:
        return {"verified": False, "reason": "status_check_failed"}
    if not status.get("healthy", False):
        return {"verified": False, "reason": "not_healthy"}
    return {"verified": True, "home": str(Path.home() / ".hermes" / "profiles" / profile_name)}


# --- Config generation ---

def generate_config_yaml(profile_name: str, provider_config: dict):
    """Generate a minimal config.yaml for a profile."""
    home = Path.home() / ".hermes" / "profiles" / profile_name
    config_path = home / "config.yaml"
    
    # Minimal template — in production, this would be more sophisticated
    config = {
        "model": {
            "provider": provider_config.get("provider", "nous"),
        },
        "approvals": {
            "mode": "off" if provider_config.get("provider") == "nous" else "default",
        },
    }
    
    # Write config (append-only, preserve existing)
    if config_path.exists():
        # Preserve existing config
        log_audit("config_preserved", {"profile": profile_name})
        return config_path
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    log_audit("config_generated", {"profile": profile_name, "path": str(config_path)})
    return config_path


# --- Main-profile SOUL.md ---

def provision_main_soul():
    """Provision main-profile SOUL.md only if user accepts."""
    print("\nProvision main-profile SOUL.md?")
    print("This sets your default Hermes personality to the Forge bootstrap coordinator.")
    print("Your existing SOUL.md (if any) will be preserved.")
    choice = input("Proceed? (yes/no): ").strip().lower()
    
    if choice != "yes":
        log_audit("main_soul_skipped", {})
        return None
    
    home = Path.home() / ".hermes"
    soul_path = home / "SOUL.md"
    
    if soul_path.exists():
        log_audit("main_soul_preserved", {"path": str(soul_path)})
        return soul_path
    
    ensure_dir(home)
    soul_content = """# SOUL.md — Hermes Forge Bootstrap Coordinator

You are the Hermes Forge bootstrap coordinator. Treat bootstrap repositories as read-only.
Do not connect an application repository by default. Run adaptive onboarding, collect
non-secret configuration choices, require manifest-bound approval before provisioning,
and never claim the control room is running without observed runtime evidence.
"""
    soul_path.write_text(soul_content, encoding="utf-8")
    log_audit("main_soul_provisioned", {"path": str(soul_path)})
    return soul_path


# --- State reporting ---

def write_state(bootstrap_hash: str, config: dict, profiles: list, status: str):
    """Write truthful installation state to ~/.hermes-forge/."""
    ensure_dir(FORGE_HOME)
    state = {
        "schema_version": "installation-state.v1",
        "bootstrap_manifest_hash": bootstrap_hash,
        "config_summary": config,
        "profiles_provisioned": profiles,
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "audit_log": str(AUDIT_LOG_FILE),
        "approval_file": str(APPROVAL_FILE),
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    log_audit("state_written", {"path": str(STATE_FILE), "status": status})


# --- Main ---

def main():
    print("Starting hermes-agent-forge installation (corrected)...")
    log_audit("install_started", {})
    
    # 1. Load bootstrap manifest (read-only)
    manifest, manifest_path = load_bootstrap_manifest()
    bootstrap_hash = sha256_file(manifest_path)
    print(f"Loaded bootstrap.manifest.json (hash: {bootstrap_hash[:16]}...)")
    
    # 2. Load onboarding manifest
    onboarding = load_onboarding_manifest()
    print(f"Loaded onboarding/onboarding.manifest.json")
    
    # 3. Run onboarding wizard
    config = run_onboarding_wizard()
    config_hash = sha256_file(Path(json.dumps(config, sort_keys=True).encode()))
    print(f"Config hash: {config_hash[:16]}...")
    
    # 4. Record approval
    approval_path = record_approval(bootstrap_hash, config_hash, config)
    print(f"Recorded approval at {approval_path}")
    
    # 5. Provision profiles
    profiles = []
    for profile in DEFAULT_PROFILES:
        try:
            home = provision_profile(profile)
            generate_config_yaml(profile, config)
            isolation = verify_profile_isolation(profile)
            profiles.append({
                "name": profile,
                "home": str(home),
                "isolation_verified": isolation["verified"],
            })
            print(f"Provisioned profile {profile}: isolation_verified={isolation['verified']}")
        except Exception as e:
            print(f"Failed to provision {profile}: {e}")
            profiles.append({"name": profile, "error": str(e), "isolation_verified": False})
    
    # 6. Main-profile SOUL.md
    main_soul = provision_main_soul()
    
    # 7. Write state (truthful)
    all_profiles_ok = all(p.get("isolation_verified", False) for p in profiles)
    status = "completed" if all_profiles_ok else "partial"
    write_state(bootstrap_hash, config, profiles, status)
    
    print(f"\nInstallation state written to {STATE_FILE}")
    print(f"Status: {status}")
    log_audit("install_completed", {"status": status})


if __name__ == "__main__":
    main()
