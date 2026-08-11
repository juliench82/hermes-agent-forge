"""Preparation layer for Hermes-native dynamic onboarding."""
from __future__ import annotations

from typing import Any

from compiler.onboarding_prompt import generate_profile_discovery_prompt, parse_hermes_response, validate_team_structure


def collect_onboarding_answers() -> dict[str, Any]:
    """Collect free-text onboarding answers; implemented in PR #37."""
    raise NotImplementedError("dynamic onboarding collection is implemented in PR #37")


def discover_profiles_via_hermes(use_case: str, user_role: str, goals: list[str]) -> dict[str, Any]:
    """Prepare discovery; Hermes execution is implemented in PR #37."""
    generate_profile_discovery_prompt(use_case, user_role, goals)
    raise NotImplementedError("Hermes subprocess orchestration is implemented in PR #37")


def create_profiles_from_team(team: dict[str, Any]) -> None:
    """Validate a team; provisioning is implemented in PR #37."""
    errors = validate_team_structure(team)
    if errors:
        raise ValueError("cannot provision invalid team: " + "; ".join(errors))
    raise NotImplementedError("profile provisioning is implemented in PR #37")
