"""
installation_state.py — Schema-backed lifecycle state machine for installation.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from enum import Enum

RUNTIME_DIR = Path("runtime")
INSTALLATION_STATE_FILE = RUNTIME_DIR / "installation_state.json"

class InstallState(str, Enum):
    NOT_STARTED = "not_started"
    PREREQS_CHECK = "prereqs_check"
    APPROVAL_RECORDED = "approval_recorded"
    PROFILES_PROVISIONED = "profiles_provisioned"
    ROLE_ASSETS_INSTALLED = "role_assets_installed"
    OBSIDIAN_SETUP = "obsidian_setup"
    BUZZ_SETUP = "buzz_setup"
    SMOKE_TESTS = "smoke_tests"
    ORCHESTRATOR_STARTED = "orchestrator_started"
    HANDOFF_PERFORMED = "handoff_performed"
    COMPLETED = "completed"
    FAILED = "failed"

def load_state():
    """Load current installation state, or return a fresh state if none exists."""
    if not INSTALLATION_STATE_FILE.exists():
        return {
            "schema_version": "installation-state.v1",
            "state": InstallState.NOT_STARTED.value,
            "steps": {},
            "updated_at": None,
        }
    with open(INSTALLATION_STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict):
    """Persist installation state."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(INSTALLATION_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def transition(state: dict, new_state: InstallState, step_details: dict):
    """Transition to a new state, recording step details."""
    state["state"] = new_state.value
    state["steps"][new_state.value] = {
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "details": step_details,
    }
    save_state(state)
    return state
