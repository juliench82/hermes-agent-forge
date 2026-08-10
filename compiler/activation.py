"""Sprint 7 activation path: bootstrap discovery to ready team summary.

This module orchestrates discovery, onboarding proposal, and team compilation.
It deliberately does not start profiles, create workspaces, connect connectors,
or connect a user project repository.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from compiler.bootstrap_discovery import BootstrapDiscovery, discover_bootstrap
from compiler.onboarding import OnboardingResult, propose_team
from compiler.team_compiler import TeamPlan, compile_team_plan

@dataclass(frozen=True)
class ActivationResult:
    discovery: BootstrapDiscovery
    onboarding: OnboardingResult
    team_plan: TeamPlan
    summary: dict[str, Any]

def activate_bootstrap(root: Path | str, answers: dict[str, Any], *, approved: bool = False) -> ActivationResult:
    discovery = discover_bootstrap(root)
    onboarding = propose_team(answers)
    team_plan = compile_team_plan(onboarding.team_manifest, approved=approved)
    summary = {
        "team": team_plan.manifest["sourceProposal"],
        "profiles": [item["profile"] for item in team_plan.manifest["profiles"]],
        "status": "active",
        "approvalMode": team_plan.manifest["approval"]["mode"],
        "bootstrapRepository": team_plan.manifest["bootstrapRepository"],
        "userProjectRepository": team_plan.manifest["userProjectRepository"],
        "runtimeReady": True,
        "provisioned": team_plan.manifest["provisioning"]["profilesStarted"],
    }
    return ActivationResult(discovery=discovery, onboarding=onboarding, team_plan=team_plan, summary=summary)
