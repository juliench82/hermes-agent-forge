"""Resolve Hermes capability labels to catalog identifiers safely."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from typing import Any, Callable

Runner = Callable[..., subprocess.CompletedProcess[str]]
_IDENTIFIER = re.compile(r"(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+(?:\?[^\s]+)?")


class SkillResolutionError(ValueError):
    """Raised when a capability cannot be resolved unambiguously."""


@dataclass(frozen=True)
class SkillCandidate:
    identifier: str
    name: str = ""
    description: str = ""


def _candidate_from_value(value: Any) -> SkillCandidate | None:
    if isinstance(value, str):
        return SkillCandidate(value.strip()) if value.strip() else None
    if not isinstance(value, dict):
        return None
    identifier = value.get("identifier") or value.get("id") or value.get("slug") or value.get("name")
    if not isinstance(identifier, str) or not identifier.strip():
        return None
    return SkillCandidate(identifier.strip(), str(value.get("name", "")), str(value.get("description", "")))


def parse_skill_search_output(output: str) -> list[SkillCandidate]:
    """Parse JSON or human-readable Hermes skill search output."""
    text = output.strip()
    if not text:
        return []
    try:
        payload = json.loads(text)
        values = payload if isinstance(payload, list) else payload.get("results", payload.get("skills", [])) if isinstance(payload, dict) else []
        candidates = [_candidate_from_value(value) for value in values]
        return [candidate for candidate in candidates if candidate is not None]
    except json.JSONDecodeError:
        identifiers = dict.fromkeys(_IDENTIFIER.findall(text))
        return [SkillCandidate(identifier) for identifier in identifiers]


def search_skill_catalog(capability: str, *, runner: Runner = subprocess.run, executable: str = "hermes") -> list[SkillCandidate]:
    """Search Hermes's catalog and return fully qualified candidates."""
    if not capability.strip():
        raise ValueError("capability must be non-empty")
    result = runner([executable, "skills", "search", capability], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SkillResolutionError(result.stderr.strip() or "skill search failed")
    return parse_skill_search_output(result.stdout)


def resolve_capability(capability: str, candidates: list[SkillCandidate]) -> SkillCandidate:
    """Resolve a capability only when the catalog result is unambiguous."""
    if not candidates:
        raise SkillResolutionError(f"no skill found for capability: {capability}")
    query = capability.casefold().strip()
    exact = [candidate for candidate in candidates if candidate.identifier.casefold() == query or candidate.name.casefold() == query]
    if len(exact) == 1:
        return exact[0]
    if len(candidates) == 1:
        return candidates[0]
    identifiers = ", ".join(candidate.identifier for candidate in candidates)
    raise SkillResolutionError(f"ambiguous skill for capability {capability}: {identifiers}")


def install_resolved_skill(profile: str, skill: SkillCandidate, *, approved: bool, runner: Runner = subprocess.run, executable: str = "hermes") -> None:
    """Install one catalog-resolved skill only after explicit approval."""
    if not approved:
        raise PermissionError(f"installation not approved for {skill.identifier}")
    result = runner([executable, "-p", profile, "skills", "install", skill.identifier], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SkillResolutionError(result.stderr.strip() or f"failed to install {skill.identifier}")
