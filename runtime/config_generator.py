"""
config_generator.py — Generate per-profile config.yaml templates.
"""

import json
from pathlib import Path

def generate_config_yaml(profile_name: str, provider_config: dict):
    """Generate a minimal config.yaml for a profile."""
    home = Path.home() / ".hermes" / "profiles" / profile_name
    config_path = home / "config.yaml"
    
    # Minimal template
    config = {
        "model": {
            "provider": provider_config.get("provider", "nous"),
        },
        "approvals": {
            "mode": "off" if provider_config.get("provider") == "nous" else "default",
        },
    }
    
    # Preserve existing config
    if config_path.exists():
        return {"path": str(config_path), "action": "preserved"}
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    return {"path": str(config_path), "action": "generated"}
