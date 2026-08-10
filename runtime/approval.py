"""
approval.py — Approval records bound to bootstrap manifest hash.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

APPROVALS_DIR = Path("approvals")

def record_installation_approval(bootstrap_manifest_path: Path, bootstrap_hash: str):
    """Record explicit approval for installation, bound to the bootstrap manifest hash."""
    APPROVALS_DIR.mkdir(parents=True, exist_ok=True)
    approval_path = APPROVALS_DIR / "installation-approval.json"
    approval = {
        "approved": True,
        "bootstrap_manifest_path": str(bootstrap_manifest_path),
        "bootstrap_manifest_hash": bootstrap_hash,
        "approved_at": datetime.now(timezone.utc).isoformat(),
        "reason": "User confirmed installation of hermes-agent-forge bootstrap repository.",
    }
    with open(approval_path, "w", encoding="utf-8") as f:
        json.dump(approval, f, indent=2)
    return approval_path


def load_installation_approval():
    """Load the installation approval record, if it exists."""
    approval_path = APPROVALS_DIR / "installation-approval.json"
    if not approval_path.exists():
        return None
    with open(approval_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_approval_for_manifest(bootstrap_hash: str):
    """Validate that the current approval is bound to the given manifest hash."""
    approval = load_installation_approval()
    if not approval:
        return False
    return approval.get("bootstrap_manifest_hash") == bootstrap_hash
