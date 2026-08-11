"""Adaptive, read-only-bootstrap Hermes Forge installer."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path
from datetime import datetime, timezone
from .hardening import write_managed_config, verify_profile, write_truthful_state
from .native_runtime import activate_yolo

PROFILES = {
  3: ["orchestrator", "builder", "quality-guardian"],
  5: ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"],
  7: ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian", "self-improver", "devops-security"],
}
FORGE_HOME = Path.home() / ".hermes-forge"
HERMES_HOME = Path.home() / ".hermes"
STATE_FILE = FORGE_HOME / "installation_state.json"


def ask(prompt, default=""):
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def yaml_scalar(value):
    return json.dumps(str(value))


def config_yaml(provider, model, profile):
    skills = [f"{profile}-role", "hermes-cli"]
    lines = [
      "_config_version: 34", "model:", f"  provider: {yaml_scalar(provider)}", f"  name: {yaml_scalar(model)}",
      "toolsets:", "  - hermes-cli", "agent:", "  max_turns: 50", "  default_personality: bootstrap-coordinator", "  reasoning_effort: high",
      "terminal:", "  backend: native", "  timeout: 120", "  home_mode: profile", "approvals:", "  mode: off",
      "platform_toolsets:", "  - cli", "skills:"] + [f"  - {yaml_scalar(x)}" for x in skills] + [
      "memory:", "  enabled: true", f"  namespace: {yaml_scalar('hermes-forge-' + profile)}", "delegation:", "  enabled: true", "  max_profiles: 7", ""
    ]
    return "\n".join(lines)


def main():
    root = Path(__file__).resolve().parents[1]
    json.loads((root / "bootstrap.manifest.json").read_text(encoding="utf-8"))
    FORGE_HOME.mkdir(parents=True, exist_ok=True)
    yolo = activate_yolo()
    if not yolo.ok:
        write_truthful_state(STATE_FILE, {"provider": None, "model": None, "team_size": None}, [], [{"step": "yolo", "command": list(yolo.command), "error": yolo.stderr or "activation failed"}])
        print("Status: partial (YOLO activation failed)")
        return 1
    print("=== Hermes Forge adaptive onboarding ===")
    use_case = ask("Use case", "software project")
    role = ask("Your role", "founder/developer")
    default_size = 3 if any(x in use_case.lower() for x in ("solo", "content")) else 7 if "enterprise" in use_case.lower() else 5
    size = int(ask("Team size (3, 5, or 7)", str(default_size)))
    if size not in PROFILES:
        raise ValueError("Team size must be 3, 5, or 7")
    provider = ask("Model provider", "nous")
    model = ask("Model", "default")
    config = {"use_case": use_case, "role": role, "team_size": size, "provider": provider, "model": model}
    profiles, errors = [], []
    for name in PROFILES[size]:
        try:
            result = subprocess.run(["hermes", "profile", "create", name], text=True, capture_output=True, check=False)
            home = HERMES_HOME / "profiles" / name
            if result.returncode and "already exists" not in result.stderr.lower():
                raise RuntimeError(result.stderr.strip() or "profile creation failed")
            home.mkdir(parents=True, exist_ok=True)
            write_managed_config(home / "config.yaml", config_yaml(provider, model, name))
            if not (home / "SOUL.md").exists():
                (home / "SOUL.md").write_text(f"# {name}\n\nHermes Forge profile.\n", encoding="utf-8")
            profiles.append({"name": name, **verify_profile(home)})
        except Exception as exc:
            errors.append({"profile": name, "error": str(exc)})
    soul = HERMES_HOME / "SOUL.md"
    if not soul.exists():
        soul.parent.mkdir(parents=True, exist_ok=True)
        soul.write_text("# Hermes Forge Bootstrap Coordinator\n\nCoordinate adaptive onboarding and report only observed status.\n", encoding="utf-8")
    status = write_truthful_state(STATE_FILE, config, profiles, errors)
    print(f"Status: {status}")
    print(f"State: {STATE_FILE}")
    return 0 if status == "completed" else 1

if __name__ == "__main__":
    raise SystemExit(main())
