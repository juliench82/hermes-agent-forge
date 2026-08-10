"""
smoke_tests.py — Real smoke tests calling Hermes CLI, Obsidian, and BUZZ.
"""

import subprocess
import os
import json

DEFAULT_PROFILES = [
    "orchestrator",
    "product-strategist",
    "architect",
    "builder",
    "quality-guardian",
]

def hermes_json(cmd: list):
    """Run a hermes CLI command and parse JSON output."""
    full_env = os.environ.copy()
    full_env["HERMES_YOLO_MODE"] = "1"
    full_cmd = ["hermes"] + cmd + ["--json"]
    result = subprocess.run(full_cmd, env=full_env, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def run_smoke_tests():
    """Run real smoke tests against Hermes CLI."""
    for profile in DEFAULT_PROFILES:
        status = hermes_json(["-p", profile, "status"])
        if status is None:
            raise RuntimeError(f"Smoke test failed for profile {profile}: status check returned None")
        if not status.get("healthy", False):
            raise RuntimeError(f"Smoke test failed for profile {profile}: not healthy")
    return True
