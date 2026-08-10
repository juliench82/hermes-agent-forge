"""Sprint 5 deterministic onboarding: answers to a proposed team manifest."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

REQUIRED_ANSWERS = {"objective", "userType", "projectStage", "workflowCategory", "projectRepositoryNeeded", "connectors", "sensitiveData", "autonomy", "approvalRequirements", "reporting"}
BASELINE_PROFILES = ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"]

class OnboardingError(ValueError):
    pass

@dataclass(frozen=True)
class OnboardingResult:
    use_case: str
    team_manifest: dict[str, Any]

def validate_answers(answers: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_ANSWERS - answers.keys())
    if missing:
        raise OnboardingError(f"missing onboarding answers: {missing}")
    if answers["userType"] != "solo-founder":
        raise OnboardingError("unsupported userType for Sprint 5")
    if not isinstance(answers["workflowCategory"], list):
        raise OnboardingError("workflowCategory must be a list")

def classify_use_case(answers: dict[str, Any]) -> str:
    validate_answers(answers)
    categories = set(answers["workflowCategory"])
    words = f"{answers['objective']} {' '.join(answers['workflowCategory'])}".lower()
    if "saas" in words or {"mvp-definition", "architecture", "implementation"}.issubset(categories):
        return "solo-founder-saas"
    raise OnboardingError("no supported Sprint 5 use case matched")

def _profile(profile_id: str) -> dict[str, Any]:
    roles = {
        "orchestrator": "plan, delegate, consolidate",
        "product-strategist": "product brief and acceptance criteria",
        "architect": "technical design and trade-offs",
        "builder": "approved implementation in isolated workspace",
        "quality-guardian": "tests, regression, security, readiness",
    }
    approvals = ["external-write", "merge", "deploy", "migration", "financial-action", "external-communication"]
    return {"id": profile_id, "role": roles[profile_id], "workspace": f"isolated/{profile_id}", "contextBoundary": "minimum-required", "allowedTools": ["read", "draft"], "forbiddenActions": approvals, "approvalRequired": approvals, "escalation": "orchestrator"}

def propose_team(answers: dict[str, Any]) -> OnboardingResult:
    use_case = classify_use_case(answers)
    manifest = {
        "apiVersion": "hermes.team/v1", "kind": "TeamManifest", "status": "proposed", "useCase": use_case,
        "team": {"name": use_case, "profiles": [_profile(profile_id) for profile_id in BASELINE_PROFILES]},
        "bootstrapRepository": {"active": True, "readOnly": True},
        "userProjectRepository": {"connected": False},
        "approval": {"mode": "human-in-the-loop", "requestedActions": answers["approvalRequirements"]},
        "sideEffects": {"provisioned": False, "connectorsConnected": False},
    }
    return OnboardingResult(use_case=use_case, team_manifest=manifest)
