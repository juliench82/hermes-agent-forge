from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .planner import DeploymentPlan


class RenderError(ValueError):
    """Raised when generated output cannot be safely rendered."""


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_agent_id(agent_id: str) -> str:
    if not agent_id or agent_id in {".", ".."} or any(part in {".", ".."} for part in Path(agent_id).parts):
        raise RenderError(f"unsafe agent id: {agent_id!r}")
    if not all(char.isalnum() or char in "-_" for char in agent_id):
        raise RenderError(f"unsafe agent id: {agent_id!r}")
    return agent_id


def _prompt(agent: dict[str, Any]) -> str:
    return "\n".join([
        f"# Agent: {agent['id']}",
        "",
        f"Purpose: {agent['purpose']}",
        "",
        "Operate only within the generated tool policy and assigned data namespace.",
        "Never access another agent's namespace or credentials.",
        "Every irreversible action requires the configured confirmation gate.",
        "All tool calls are audited.",
        "",
    ])


def render_plan(plan: DeploymentPlan, output_dir: Path) -> Path:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    root = output_dir / plan.tenantId
    root.mkdir(parents=True, exist_ok=True)

    _write_json(root / "plan.json", plan.to_dict())
    _write_json(root / "manifest.json", {
        "kind": "GeneratedTenantBundle",
        "version": "1.0.0",
        "tenantId": plan.tenantId,
        "sourcePlanFingerprint": plan.fingerprint,
        "providerNeutral": True,
        "secretValuesIncluded": False,
    })
    _write_json(root / "isolation" / "agents.json", {
        "tenantId": plan.tenantId,
        "agents": [
            {"agentId": agent["id"], "dataNamespace": agent["isolation"]["dataNamespace"], "networkPolicy": agent["isolation"]["networkPolicy"], "filesystem": agent["isolation"]["filesystem"]}
            for agent in plan.agents
        ],
    })
    _write_json(root / "coordination" / "delegation.json", {"edges": plan.delegation})
    _write_json(root / "secrets.manifest.json", {
        "providerNeutral": True,
        "references": sorted({ref for connector in plan.connectors for ref in connector["secretRefs"]}),
        "valuesIncluded": False,
    })

    for agent in plan.agents:
        agent_id = _safe_agent_id(agent["id"])
        agent_root = root / "agents" / agent_id
        _write_json(agent_root / "hermes.json", {
            "agentId": agent["id"],
            "profile": agent["profile"],
            "purpose": agent["purpose"],
            "providerNeutral": True,
        })
        _write_json(agent_root / "tools-policy.json", {
            "agentId": agent["id"],
            "connectors": agent["connectors"],
            "permissions": agent["permissions"],
        })
        (agent_root / "system-prompt.md").write_text(_prompt(agent), encoding="utf-8")
    return root
