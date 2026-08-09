from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from runtime.tenant_spec import validate_file

from .catalog import Catalog
from .errors import CompilerError


@dataclass(frozen=True)
class DeploymentPlan:
    planVersion: str
    tenantId: str
    specVersion: str
    baseline: dict[str, Any]
    primitives: list[dict[str, Any]]
    agents: list[dict[str, Any]]
    connectors: list[dict[str, Any]]
    delegation: list[dict[str, str]]
    fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_spec(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CompilerError(f"cannot load TenantSpec: {exc}") from exc


def build_plan(spec_path: Path, catalog: Catalog | None = None) -> DeploymentPlan:
    validate_file(spec_path)
    spec = _read_spec(spec_path)
    catalog = catalog or Catalog()

    baseline = catalog.resolve(spec["security"]["baseline"])
    connector_refs = [connector["primitive"] for connector in spec["connectors"]]
    profile_refs = [agent["profile"] for agent in spec["agents"]]
    primitive_refs = [baseline["reference"], *connector_refs, *profile_refs]

    trigger_refs: list[str] = []
    for agent in spec["agents"]:
        for trigger in agent.get("triggers", []):
            if isinstance(trigger, dict) and trigger.get("primitive"):
                trigger_refs.append(trigger["primitive"])
    primitives = catalog.resolve_many([*primitive_refs, *trigger_refs])

    connector_map = {connector["id"]: connector for connector in spec["connectors"]}
    connectors = []
    for connector in sorted(spec["connectors"], key=lambda item: item["id"]):
        connectors.append({
            "id": connector["id"],
            "primitive": connector["primitive"],
            "secretRefs": sorted(connector["secretRefs"]),
            "allowedOperations": sorted(connector["allowedOperations"]),
        })

    agents = []
    delegation = []
    for agent in sorted(spec["agents"], key=lambda item: item["id"]):
        bindings = []
        for binding in sorted(agent["connectors"], key=lambda item: item["connectorId"]):
            if binding["connectorId"] not in connector_map:
                raise CompilerError(f"agent {agent['id']}: unknown connector {binding['connectorId']}")
            bindings.append({"connectorId": binding["connectorId"], "scopes": sorted(binding["scopes"])})
        agents.append({
            "id": agent["id"],
            "profile": agent["profile"],
            "purpose": agent["purpose"],
            "isolation": agent["isolation"],
            "connectors": bindings,
            "permissions": agent["permissions"],
        })
        for target in sorted(agent.get("delegates", {}).get("allow", [])):
            delegation.append({"from": agent["id"], "to": target})

    draft = {
        "planVersion": "1.0.0",
        "tenantId": spec["metadata"]["tenantId"],
        "specVersion": spec["metadata"]["specVersion"],
        "baseline": baseline,
        "primitives": primitives,
        "agents": agents,
        "connectors": connectors,
        "delegation": delegation,
    }
    canonical = json.dumps(draft, sort_keys=True, separators=(",", ":")).encode()
    fingerprint = hashlib.sha256(canonical).hexdigest()
    return DeploymentPlan(fingerprint=fingerprint, **draft)
