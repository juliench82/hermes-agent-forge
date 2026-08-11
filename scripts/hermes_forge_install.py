#!/usr/bin/env python3
"""Hermes-native generic onboarding installer entrypoint."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.onboarding_lifecycle import (
    OnboardingAnswers,
    collect_onboarding_answers,
    execute_onboarding_plan,
    prepare_onboarding_plan,
)

FORGE_HOME = Path(os.environ.get("HERMES_FORGE_HOME", Path.home() / ".hermes-forge"))
STATE_FILE = FORGE_HOME / "installation_state.json"
COMMAND_TIMEOUT = 120


def load_bootstrap_manifest() -> dict[str, Any]:
    return json.loads((ROOT / "bootstrap.manifest.json").read_text(encoding="utf-8"))


def load_onboarding_manifest() -> dict[str, Any]:
    return json.loads((ROOT / "onboarding" / "onboarding.manifest.json").read_text(encoding="utf-8"))


def hermes_cli(command: list[str], *, timeout: int = COMMAND_TIMEOUT) -> subprocess.CompletedProcess[str]:
    """Run one Hermes command without shell interpolation."""
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    timeout = kwargs.pop("timeout", COMMAND_TIMEOUT)
    kwargs.pop("check", None)
    return hermes_cli(command, timeout=timeout)


def _plan_for_display(plan: dict[str, Any]) -> dict[str, Any]:
    team = plan["team"]
    resolved = plan["resolved_skills"]
    profiles = []
    for profile in team["profiles"]:
        name = profile["name"]
        profiles.append({
            "name": name,
            "description": profile["description"],
            "capabilities": profile["skills"],
            "resolved_skills": [candidate.identifier for candidate in resolved[name]],
            "files": [
                f"~/.hermes/profiles/{name}/config.yaml",
                f"~/.hermes/profiles/{name}/SOUL.md",
            ],
        })
    return {
        "team_size": team["team_size"],
        "profiles": profiles,
        "approval_required": True,
    }


def render_plan(plan: dict[str, Any]) -> str:
    return json.dumps(_plan_for_display(plan), indent=2, sort_keys=True)


def _write_state(status: str, *, answers: OnboardingAnswers | None = None, plan: dict[str, Any] | None = None, results: list[dict[str, Any]] | None = None, error: str | None = None) -> None:
    FORGE_HOME.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {"status": status}
    if answers is not None:
        payload["answers"] = {
            "use_case": answers.use_case,
            "user_role": answers.user_role,
            "goals": answers.goals,
            "team_size_preference": answers.team_size_preference,
        }
    if plan is not None:
        payload["plan"] = _plan_for_display(plan)
    if results is not None:
        payload["results"] = results
    if error is not None:
        payload["error"] = error
    STATE_FILE.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def approve_plan(plan: dict[str, Any], input_fn: Callable[[str], str] = input) -> bool:
    print("\nProposed Hermes onboarding plan:\n")
    print(render_plan(plan))
    answer = input_fn("Approve this exact plan? [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def main(input_fn: Callable[[str], str] = input) -> int:
    answers: OnboardingAnswers | None = None
    try:
        load_bootstrap_manifest()
        load_onboarding_manifest()
        answers = collect_onboarding_answers(input_fn)
        plan = prepare_onboarding_plan(answers, runner=_runner)
    except Exception as exc:
        print(f"Onboarding stopped before provisioning: {exc}", file=sys.stderr)
        return 1

    if not approve_plan(plan, input_fn):
        print("Onboarding plan rejected; no profiles, skills, or assets were created.")
        return 2

    try:
        results = execute_onboarding_plan(plan, approved=True, runner=_runner)
    except Exception as exc:
        _write_state("failed", answers=answers, plan=plan, error=str(exc))
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1

    failed = [result for result in results if not result.get("verified", True)]
    status = "partial" if failed else "completed"
    _write_state(status, answers=answers, plan=plan, results=results)
    print(f"Installation status: {status}")
    print(f"State file: {STATE_FILE}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
