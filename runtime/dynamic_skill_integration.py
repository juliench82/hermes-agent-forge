"""Validated capability resolution and skill installation pipeline."""
from __future__ import annotations

from typing import Any, Callable, Sequence

from compiler.onboarding_prompt import validate_team_structure
from runtime.skill_resolution import SkillCandidate, install_resolved_skill, resolve_capability, search_skill_catalog


class SkillPipelineError(ValueError):
    """Raised when capability preflight or approval fails."""


def resolve_team_capabilities(team: dict[str, Any], *, searcher: Callable[[str], list[SkillCandidate]] = search_skill_catalog) -> dict[str, list[SkillCandidate]]:
    """Resolve every team capability before any profile side effect."""
    errors = validate_team_structure(team)
    if errors:
        raise SkillPipelineError("invalid team: " + "; ".join(errors))
    resolved: dict[str, list[SkillCandidate]] = {}
    for profile in team["profiles"]:
        candidates: list[SkillCandidate] = []
        for capability in profile["skills"]:
            try:
                candidates.append(resolve_capability(capability, searcher(capability)))
            except ValueError as exc:
                raise SkillPipelineError(f"{profile['name']}: {exc}") from exc
        resolved[profile["name"]] = candidates
    return resolved


def install_team_skills(resolved: dict[str, Sequence[SkillCandidate]], *, approved: bool, installer: Callable[..., None] = install_resolved_skill) -> None:
    """Install pre-resolved skills only after explicit approval."""
    if not approved:
        raise PermissionError("skill installation requires explicit approval")
    for profile, skills in resolved.items():
        for skill in skills:
            installer(profile, skill, approved=True)
