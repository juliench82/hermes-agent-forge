#!/usr/bin/env python3
"""Hermes-native generic onboarding installer entrypoint."""
from __future__ import annotations

import hashlib
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


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_bootstrap_manifest() -> tuple[dict[str, Any], Path]:
    path = ROOT / "bootstrap.manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    required = ("schema_version", "repo_kind", "default_team", "installer_entrypoint", "installer_command")
    missing = [field for field in required if field not in manifest]
    if missing:
        raise ValueError(f"Missing required manifest fields: {', '.join(missing)}")
    if manifest["repo_kind"] != "bootstrap":
        raise ValueError("repo_kind must be bootstrap")
    return manifest, path


def load_onboarding_manifest() -> dict[str, Any]:
    return json.loads((ROOT / "onboarding" / "onboarding.manifest.json").read_text(encoding="utf-8"))


def hermes_cli(cmd: list[str], check: bool = True, *, timeout: int = COMMAND_TIMEOUT) -> subprocess.CompletedProcess[str]:
    command = list(cmd)
    if not command or command[0] != "hermes":
        command.insert(0, "hermes")
    return subprocess.run(command, check=check, capture_output=True, text=True, timeout=timeout)


def _runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    timeout = kwargs.pop("timeout", COMMAND_TIMEOUT)
    check = kwargs.pop("check", False)
    return hermes_cli(command, check=check, timeout=timeout)


def hermes_json(cmd: list[str]) -> dict[str, Any] | None:
    result = hermes_cli([*cmd, "--json"], check=False)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def generate_config_yaml(profile_name: str, provider_config: dict[str, Any]) -> Path:
    from runtime.adaptive_installer import config_yaml
    path = Path.home() / ".hermes" / "profiles" / profile_name / "config.yaml"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(config_yaml(provider_config.get("provider", "nous"), provider_config.get("model", "default"), profile_name), encoding="utf-8")
    return path


def record_approval(bootstrap_hash: str, config_hash: str = "", config: dict[str, Any] | None = None) -> Path:
    ensure_dir(FORGE_HOME)
    path = FORGE_HOME / "approval.json"
    path.write_text(json.dumps({"approved": True, "bootstrap_manifest_hash": bootstrap_hash, "config_hash": config_hash, "config_summary": config or {}}, indent=2), encoding="utf-8")
    return path


def write_installation_state(bootstrap_hash: str, approval_path: Path | None = None, version_line: str = "") -> Path:
    ensure_dir(FORGE_HOME)
    state = {"schema_version": "installation-state.v1", "bootstrap_manifest_hash": bootstrap_hash, "approval_path": str(approval_path) if approval_path else None, "hermes_version_line": version_line, "status": "partial"}
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return STATE_FILE


def run_onboarding_wizard() -> dict[str, Any]:
    answers = collect_onboarding_answers()
    return {"use_case": answers.use_case, "role": answers.user_role, "goals": answers.goals, "team_size": answers.team_size_preference}


def _plan_for_display(plan: dict[str, Any]) -> dict[str, Any]:
    team = plan["team"]
    resolved = plan["resolved_skills"]
    profiles = []
    for profile in team["profiles"]:
        name = profile["name"]
        profiles.append({"name": name, "description": profile["description"], "capabilities": profile["skills"], "resolved_skills": [candidate.identifier for candidate in resolved[name]], "files": [f"~/.hermes/profiles/{name}/config.yaml", f"~/.hermes/profiles/{name}/SOUL.md"]})
    return {"team_size": team["team_size"], "profiles": profiles, "approval_required": True}


def render_plan(plan: dict[str, Any]) -> str:
    return json.dumps(_plan_for_display(plan), indent=2, sort_keys=True)


def _write_state(status: str, *, answers: OnboardingAnswers | None = None, plan: dict[str, Any] | None = None, results: list[dict[str, Any]] | None = None, error: str | None = None) -> None:
    ensure_dir(FORGE_HOME)
    payload: dict[str, Any] = {"status": status}
    if answers is not None:
        payload["answers"] = {"use_case": answers.use_case, "user_role": answers.user_role, "goals": answers.goals, "team_size_preference": answers.team_size_preference}
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
    return input_fn("Approve this exact plan? [y/N] ").strip().lower() in {"y", "yes"}


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
