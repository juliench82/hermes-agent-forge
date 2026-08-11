"""
state_store.py — Installation state storage outside the bootstrap repo.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

FORGE_HOME = Path.home() / ".hermes-forge"
STATE_FILE = FORGE_HOME / "installation_state.json"
AUDIT_LOG_FILE = FORGE_HOME / "audit_log.jsonl"
APPROVAL_FILE = FORGE_HOME / "approval.json"

def ensure_forge_home():
    """Ensure ~/.hermes-forge/ exists."""
    FORGE_HOME.mkdir(parents=True, exist_ok=True)

def log_audit(event: str, details: dict):
    """Append an audit record to the audit log file."""
    ensure_forge_home()
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "details": details,
    }
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def write_state(bootstrap_hash: str, config: dict, profiles: list, status: str):
    """Write truthful installation state to ~/.hermes-forge/."""
    ensure_forge_home()
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

def record_approval(bootstrap_hash: str, config_hash: str, config: dict):
    """Record explicit approval bound to bootstrap manifest + config hash."""
    ensure_forge_home()
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
