"""Generic Hermes onboarding plan and side-effect execution lifecycle."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from runtime.dynamic_profiles import create_profiles_from_team, discover_profiles_via_hermes
from runtime.dynamic_skill_integration import resolve_team_capabilities
from runtime.skill_resolution import SkillCandidate


@dataclass(frozen=True)
class OnboardingAnswers:
    use_case: str
    user_role: str
    goals: list[str]
    team_size_preference: int | None = None


def collect_onboarding_answers(input_fn: Callable[[str], str] = input) -> OnboardingAnswers:
    """Collect generic free-text onboarding answers."""
    use_case = input_fn("What would you like Hermes to help accomplish? ").strip()
    user_role = input_fn("What is your role in this project? ").strip()
    goals: list[str] = []
    while True:
        goal = input_fn("Goal (leave blank when finished): ").strip()
        if not goal:
            break
        goals.append(goal)
    preference = input_fn("Preferred team size (3, 5, 7, or recommend): ").strip().lower()
    team_size = None if preference in ("", "recommend") else int(preference)
    if not use_case or not user_role or not goals:
        raise ValueError("use case, role, and at least one goal are required")
    if team_size is not None and team_size not in (3, 5, 7):
        raise ValueError("team size must be 3, 5, 7, or recommend")
    return OnboardingAnswers(use_case, user_role, goals, team_size)


def prepare_onboarding_plan(answers: OnboardingAnswers, *, runner: Any = None) -> dict[str, Any]:
    """Discover a team and resolve all capabilities without side effects."""
    discovery_kwargs = {}
    if runner is not None:
        discovery_kwargs["runner"] = runner
    team = discover_profiles_via_hermes(answers.use_case, answers.user_role, answers.goals, answers.team_size_preference, **discovery_kwargs)
    searcher = None
    if runner is not None:
        from runtime.skill_resolution import search_skill_catalog
        searcher = lambda capability: search_skill_catalog(capability, runner=runner)
    resolved = resolve_team_capabilities(team, **({"searcher": searcher} if searcher else {}))
    return {"answers": answers, "team": team, "resolved_skills": resolved}


def execute_onboarding_plan(plan: dict[str, Any], *, approved: bool, profile_root: Path | None = None, runner: Any = None) -> list[dict[str, Any]]:
    """Execute an approved plan; no external side effects occur otherwise."""
    if not approved:
        raise PermissionError("onboarding plan execution requires explicit approval")
    team = plan["team"]
    resolved: dict[str, list[SkillCandidate]] = plan["resolved_skills"]
    skill_ids = {name: [skill.identifier for skill in skills] for name, skills in resolved.items()}
    kwargs: dict[str, Any] = {"skills_by_profile": skill_ids, "profile_root": profile_root}
    if runner is not None:
        kwargs["runner"] = runner
    return create_profiles_from_team(team, **kwargs)
