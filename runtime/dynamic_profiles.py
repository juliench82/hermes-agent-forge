"""Hermes-native dynamic profile discovery and provisioning."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable, Sequence

from compiler.onboarding_prompt import generate_profile_discovery_prompt, parse_hermes_response, validate_team_structure

Runner = Callable[..., subprocess.CompletedProcess[str]]


class HermesCommandError(RuntimeError):
    """Raised when the Hermes CLI cannot complete a request."""


def _run_query(prompt: str, runner: Runner, executable: str, timeout: int) -> str:
    result = runner([executable, "chat", "-q", prompt, "-Q"], capture_output=True, text=True, check=False, timeout=timeout)
    if result.returncode != 0:
        raise HermesCommandError(result.stderr.strip() or "Hermes chat failed")
    if not result.stdout.strip():
        raise HermesCommandError("Hermes returned an empty response")
    return result.stdout


def discover_profiles_via_hermes(use_case: str, user_role: str, goals: list[str], team_size_preference: int | None = None, *, runner: Runner = subprocess.run, executable: str = "hermes", timeout: int = 120, max_attempts: int = 3) -> dict[str, Any]:
    """Discover and validate a team, retrying invalid model output."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    prompt = generate_profile_discovery_prompt(use_case, user_role, goals, team_size_preference)
    last_error = ""
    for attempt in range(max_attempts):
        try:
            team = parse_hermes_response(_run_query(prompt, runner, executable, timeout))
            errors = team.get("validation_errors", [])
            if errors:
                raise ValueError("; ".join(errors))
            return team
        except (HermesCommandError, ValueError) as exc:
            last_error = str(exc)
            if attempt + 1 == max_attempts:
                break
            prompt = f"{prompt}\n\nYour previous response was invalid: {last_error}. Return a corrected JSON object only."
    raise HermesCommandError(f"unable to obtain a valid team after {max_attempts} attempts: {last_error}")


def render_soul(profile: dict[str, Any]) -> str:
    """Render deterministic profile instructions from validated profile data."""
    skills = "\n".join(f"- {skill}" for skill in profile["skills"])
    return (f"# {profile['name']}\n\n## Role\n\n{profile['description']}\n\n## Capabilities\n\n{skills}\n\n## Operating principles\n\n- Focus on the assigned role and state assumptions.\n- Hand off work outside this role to the appropriate teammate.\n- Preserve user control for external and irreversible actions.\n")


def create_profiles_from_team(team: dict[str, Any], *, runner: Runner = subprocess.run, executable: str = "hermes", profile_root: Path | None = None, skills_by_profile: dict[str, Sequence[str]] | None = None) -> list[dict[str, Any]]:
    """Validate and create profiles, writing deterministic SOUL.md files."""
    errors = validate_team_structure(team)
    if errors:
        raise ValueError("cannot provision invalid team: " + "; ".join(errors))
    results: list[dict[str, Any]] = []
    for profile in team["profiles"]:
        name = profile["name"]
        command = [executable, "profile", "create", name, "--description", profile["description"]]
        result = runner(command, capture_output=True, text=True, check=False)
        if result.returncode != 0 and "already exists" not in result.stderr.lower():
            raise HermesCommandError(result.stderr.strip() or f"failed to create profile {name}")
        if skills_by_profile and skills_by_profile.get(name):
            skill_command = [executable, "-p", name, "skills", "install", *skills_by_profile[name]]
            skill_result = runner(skill_command, capture_output=True, text=True, check=False)
            if skill_result.returncode != 0:
                raise HermesCommandError(skill_result.stderr.strip() or f"failed to install skills for {name}")
        if profile_root is not None:
            home = profile_root / name
            home.mkdir(parents=True, exist_ok=True)
            (home / "SOUL.md").write_text(render_soul(profile), encoding="utf-8")
        results.append({"name": name, "skills": list(skills_by_profile.get(name, ())) if skills_by_profile else []})
    return results
