"""Sprint 6 compiler: approved onboarding proposal to executable team plan."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

BASELINE_PROFILES = ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"]
IRREVERSIBLE_ACTIONS = ["external-write", "merge", "deploy", "migration", "financial-action", "external-communication"]

class TeamCompilerError(ValueError):
    pass

@dataclass(frozen=True)
class TeamPlan:
    manifest: dict[str, Any]

def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TeamCompilerError(message)

def compile_team_plan(proposal: dict[str, Any], *, approved: bool = False) -> TeamPlan:
    _require(approved, "team proposal requires explicit approval before compilation")
    _require(proposal.get("status") == "proposed", "only proposed team manifests can be compiled")
    _require(proposal.get("useCase") == "solo-founder-saas", "unsupported Sprint 6 use case")
    _require(proposal.get("bootstrapRepository") == {"active": True, "readOnly": True}, "bootstrap repository must be active and read-only")
    _require(proposal.get("userProjectRepository", {}).get("connected") is False, "user project repository must remain disconnected")
    source_profiles = [item.get("id") for item in proposal.get("team", {}).get("profiles", [])]
    _require(source_profiles == BASELINE_PROFILES, "proposal must contain the baseline profile set in order")

    instances = []
    for profile_id in BASELINE_PROFILES:
        instances.append({
            "id": f"{profile_id}-1",
            "profile": profile_id,
            "role": next(item["role"] for item in proposal["team"]["profiles"] if item["id"] == profile_id),
            "workspace": f"isolated/{profile_id}",
            "contextBoundary": "minimum-required",
            "allowedTools": ["read", "draft"],
            "forbiddenActions": list(IRREVERSIBLE_ACTIONS),
            "approvalRequired": list(IRREVERSIBLE_ACTIONS),
            "escalation": "orchestrator-1" if profile_id != "orchestrator" else "human-owner",
        })

    manifest = {
        "apiVersion": "hermes.team-plan/v1",
        "kind": "TeamPlan",
        "status": "compiled",
        "sourceProposal": "solo-founder-saas",
        "profiles": instances,
        "communication": {
            "topology": "orchestrator-led",
            "orchestrator": "orchestrator-1",
            "specialists": [f"{profile_id}-1" for profile_id in BASELINE_PROFILES if profile_id != "orchestrator"],
            "directSpecialistMessaging": False,
        },
        "approval": {"mode": "human-in-the-loop", "gateway": "runtime.confirmation.ApprovalGateway", "irreversibleActions": list(IRREVERSIBLE_ACTIONS)},
        "enforcement": {
            "policyProxy": "runtime.policy_proxy.PolicyProxy",
            "auditLog": "runtime.audit_log.FileAuditLog",
            "isolation": "runtime.isolation.IsolationConfig",
            "secrets": "runtime.secrets.SecretsPolicy",
        },
        "bootstrapRepository": {"active": True, "readOnly": True},
        "userProjectRepository": {"connected": False},
        "provisioning": {"workspacesCreated": False, "profilesStarted": False, "connectorsConnected": False},
    }
    return TeamPlan(manifest=manifest)
