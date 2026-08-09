"""Hermes adapter for solo-founder compatibility.

This adapter maps a DeploymentPlan to a Hermes-specific compatibility bundle.
It preserves the six existing profile.yaml and skill.md files unchanged.
"""

import hashlib
import json
from typing import Any, Dict, List

CONTRACT_VERSION = "v1-draft"


def create_hermes_bundle(deployment_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Create a Hermes compatibility bundle from a DeploymentPlan.
    
    Args:
        deployment_plan: A validated DeploymentPlan from the compiler.
        
    Returns:
        A Hermes compatibility bundle with contract_version, contract_status,
        fingerprint, runtime, coordination, and manifest sections.
    """
    agents = deployment_plan.get("agents", [])
    
    runtime_agents = []
    for agent in agents:
        runtime_agents.append({
            "name": agent.get("name", ""),
            "profile": agent.get("profile", ""),
            "profile_version": agent.get("profile_version", "1.0.0"),
            "skills": agent.get("skills", []),
            "mode": "skill-routed",
            "isolation_namespace": f"{agent.get('name', 'agent')}-ns",
            "secrets": agent.get("secrets", [])
        })
    
    delegation = deployment_plan.get("delegation", [])
    handoff = deployment_plan.get("handoff", {})
    
    bundle = {
        "contract_version": CONTRACT_VERSION,
        "contract_status": "compatibility",
        "fingerprint": "",
        "runtime": {"agents": runtime_agents},
        "coordination": {"delegation": delegation, "handoff": handoff},
        "manifest": {
            "isolation": {"network": "default-deny", "filesystem": "isolated", "memory": "private"},
            "secrets_policy": deployment_plan.get("secrets_policy", []),
            "tools_policy": deployment_plan.get("tools_policy", [])
        }
    }
    
    bundle_json = json.dumps(bundle, sort_keys=True, separators=(",", ":"))
    bundle["fingerprint"] = hashlib.sha256(bundle_json.encode()).hexdigest()
    
    return bundle


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m compiler.hermes_adapter SPEC.json")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    bundle = create_hermes_bundle(spec)
    print(json.dumps(bundle, indent=2))
