from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .planner import DeploymentPlan


class HermesAdapterError(ValueError):
    pass


LEGACY_PROFILES = (
    "orchestrator",
    "product-strategist",
    "architect",
    "builder",
    "quality-guardian",
    "self-improver",
)

DEFAULT_PROFILE_MAP = {
    "orchestrator": "orchestrator",
    "product-strategist": "product-strategist",
    "architect": "architect",
    "builder": "builder",
    "quality-guardian": "quality-guardian",
    "self-improver": "self-improver",
}

STAGES = (
    ("intake", "orchestrator"),
    ("brief", "product-strategist"),
    ("design", "architect"),
    ("build", "builder"),
    ("validate", "quality-guardian"),
    ("deliver", "orchestrator"),
    ("improve", "self-improver"),
)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _profile_contract(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise HermesAdapterError(f"missing legacy profile: {path}")
    values: dict[str, Any] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith(" "):
            if line.strip().startswith("- ") and current:
                values.setdefault(current, []).append(line.strip()[2:])
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            values[current] = value.strip() or []
    return values


def _agent(plan_agent: dict[str, Any], legacy_name: str, repo_root: Path) -> dict[str, Any]:
    profile_path = repo_root / "profiles" / legacy_name / "profile.yaml"
    contract = _profile_contract(profile_path)
    for required in ("name", "purpose", "version"):
        if required not in contract:
            raise HermesAdapterError(f"legacy profile {legacy_name} missing {required}")
    return {
        "id": plan_agent["id"],
        "legacyProfile": legacy_name,
        "profileVersion": str(contract["version"]),
        "profilePath": f"profiles/{legacy_name}/profile.yaml",
        "skillPath": f"profiles/{legacy_name}/skill.md",
        "purpose": contract["purpose"],
        "inputs": contract.get("inputs", []),
        "outputs": contract.get("outputs", []),
        "allowedTools": contract.get("allowed_tools", []),
        "requiresApprovalFor": contract.get("requires_approval_for", []),
        "skills": contract.get("skills", []),
        "namespace": plan_agent["isolation"]["dataNamespace"],
    }


def render_hermes(plan: DeploymentPlan, output_dir: Path, repo_root: Path | None = None, profile_map: dict[str, str] | None = None) -> Path:
    repo_root = (repo_root or Path(__file__).resolve().parents[1]).resolve()
    profile_map = profile_map or DEFAULT_PROFILE_MAP
    root = output_dir.resolve() / plan.tenantId / "hermes"
    root.mkdir(parents=True, exist_ok=True)
    by_id = {agent["id"]: agent for agent in plan.agents}
    missing = set(profile_map) - set(by_id)
    if missing:
        raise HermesAdapterError(f"compatibility fixture missing agents: {sorted(missing)}")
    agents = [_agent(by_id[name], legacy_name, repo_root) for name, legacy_name in profile_map.items()]
    for item in agents:
        destination = root / "profiles" / item["legacyProfile"]
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo_root / item["profilePath"], destination / "profile.yaml")
        shutil.copyfile(repo_root / item["skillPath"], destination / "skill.md")
    runtime = {
        "apiVersion": "hermes.runtime/v1",
        "kind": "HermesRuntimeConfiguration",
        "adapter": "hermes",
        "adapterVersion": "1.0.0",
        "contractStatus": "compatibility",
        "tenantId": plan.tenantId,
        "rootAgent": "orchestrator",
        "routingMode": "skill-routed",
        "agents": agents,
    }
    coordination = {
        "apiVersion": "hermes.runtime/v1",
        "kind": "HermesCoordinationConfiguration",
        "workflow": "solo-founder-app-builder",
        "stages": [{"id": stage, "agent": agent} for stage, agent in STAGES],
        "delegation": plan.delegation,
        "handoffContract": "shared/profile-contract.md",
        "policyContracts": ["shared/workflows.md", "shared/safety-gates.md", "shared/safety-enforcement.md"],
    }
    _write_json(root / "runtime.json", runtime)
    _write_json(root / "coordination.json", coordination)
    manifest = {"kind": "HermesCompatibilityBundle", "version": "1.0.0", "tenantId": plan.tenantId, "secretValuesIncluded": False, "sourcePlanFingerprint": plan.fingerprint}
    _write_json(root / "manifest.json", manifest)
    fingerprint = hashlib.sha256(json.dumps({"runtime": runtime, "coordination": coordination, "manifest": manifest}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    (root / "fingerprint.sha256").write_text(fingerprint + "\n", encoding="utf-8")
    return root
