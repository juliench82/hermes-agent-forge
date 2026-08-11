"""Hermes-native onboarding prompt generation and response validation."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List

_ALLOWED_TEAM_SIZES = (3, 5, 7)
_PROFILE_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def generate_profile_discovery_prompt(use_case_description: str, user_role: str, goals: List[str], team_size_preference: int | None = None) -> str:
    """Generate a deterministic prompt for Hermes dynamic team discovery."""
    if team_size_preference is not None and team_size_preference not in _ALLOWED_TEAM_SIZES:
        raise ValueError("team_size_preference must be 3, 5, 7, or None")
    goals_text = "\n".join(f"- {goal}" for goal in goals)
    size_instruction = f"Use exactly {team_size_preference} profiles." if team_size_preference is not None else "Recommend exactly 3, 5, or 7 profiles based on complexity."
    return f"""You are designing a dynamic Hermes multi-agent team.

Use case:
{use_case_description}

User role:
{user_role}

Goals:
{goals_text}

Task:
Analyze the context and propose the smallest effective team. {size_instruction}

Requirements:
- Return between 3 and 7 profiles, with team_size matching the array length.
- Use unique, descriptive lowercase profile names containing only letters, numbers, hyphens, or underscores.
- Give each profile a concise 1-2 sentence description of responsibilities.
- Give each profile 2-4 use-case-specific capability labels in skills.
- Account for responsibilities owned by the user; do not duplicate them unnecessarily.
- Do not use a predefined use-case catalog or assume a fixed team.

Output:
Return exactly one JSON object, optionally inside a ```json code block, with this shape:
{{
  "team_size": 5,
  "profiles": [
    {{
      "name": "example-role",
      "description": "Describe the role's responsibilities.",
      "skills": ["capability-one", "capability-two"]
    }}
  ]
}}

Constraints:
- team_size must be one of 3, 5, or 7.
- profiles must contain exactly team_size items and no more than 7 items.
- Do not include commentary outside the JSON object when possible.
"""


def _extract_json_object(response_text: str) -> Dict[str, Any]:
    fenced = re.search(r"```(?:json)?\s*(\{{.*?\}})\s*```", response_text, re.DOTALL | re.IGNORECASE)
    candidate = fenced.group(1) if fenced else response_text
    decoder = json.JSONDecoder()
    for index, char in enumerate(candidate):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(candidate[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError("Hermes response does not contain a valid JSON object")


def parse_hermes_response(response_text: str) -> Dict[str, Any]:
    """Extract and validate a Hermes team response."""
    if not isinstance(response_text, str) or not response_text.strip():
        raise ValueError("Hermes response is empty")
    team = _extract_json_object(response_text)
    team["validation_errors"] = validate_team_structure(team)
    return team


def validate_team_structure(team: Dict[str, Any]) -> List[str]:
    """Return validation errors for a proposed dynamic team."""
    errors: List[str] = []
    if not isinstance(team, dict):
        return ["team must be a JSON object"]
    team_size = team.get("team_size")
    if isinstance(team_size, bool) or not isinstance(team_size, int) or team_size not in _ALLOWED_TEAM_SIZES:
        errors.append("team_size must be 3, 5, or 7")
    profiles = team.get("profiles")
    if not isinstance(profiles, list):
        return errors + ["profiles must be an array"]
    if len(profiles) > 7:
        errors.append("profile count cannot exceed 7")
    if isinstance(team_size, int) and not isinstance(team_size, bool) and len(profiles) != team_size:
        errors.append(f"profile count ({len(profiles)}) must equal team_size ({team_size})")
    names: set[str] = set()
    for index, profile in enumerate(profiles):
        prefix = f"profiles[{index}]"
        if not isinstance(profile, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = profile.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix}.name must be non-empty")
        elif not _PROFILE_NAME.fullmatch(name):
            errors.append(f"{prefix}.name is not a safe profile name")
        elif name.casefold() in names:
            errors.append(f"{prefix}.name must be unique")
        else:
            names.add(name.casefold())
        if not isinstance(profile.get("description"), str) or not profile["description"].strip():
            errors.append(f"{prefix}.description must be non-empty")
        skills = profile.get("skills")
        if not isinstance(skills, list) or not skills or any(not isinstance(skill, str) or not skill.strip() for skill in skills):
            errors.append(f"{prefix}.skills must contain at least one non-empty string")
    return errors
