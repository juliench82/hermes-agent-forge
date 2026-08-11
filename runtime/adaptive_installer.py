"""Adaptive, read-only-bootstrap Hermes Forge installer."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path
from datetime import datetime, timezone

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


def append_config(path, generated):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(generated, encoding="utf-8")
        return "generated"
    existing = path.read_text(encoding="utf-8")
    missing = [line for line in generated.splitlines(True) if line not in existing]
    if missing:
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\n# Hermes Forge managed additions\n")
            handle.writelines(missing)
        return "appended"
    return "preserved"


def write_state(status, config, profiles, errors):
    FORGE_HOME.mkdir(parents=True, exist_ok=True)
    state = {"schema_version": "installation-state.v1", "status": status, "config_summary": {"provider": config["provider"], "model": config["model"], "team_size": config["team_size"]}, "profiles_provisioned": profiles, "errors": errors, "updated_at": datetime.now(timezone.utc).isoformat()}
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, STATE_FILE)


def main():
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "bootstrap.manifest.json"
    json.loads(manifest_path.read_text(encoding="utf-8"))
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
            action = append_config(home / "config.yaml", config_yaml(provider, model, name))
            profiles.append({"name": name, "config": str(home / "config.yaml"), "config_action": action, "verified": home.exists()})
        except Exception as exc:
            errors.append({"profile": name, "error": str(exc)})
    soul = HERMES_HOME / "SOUL.md"
    if not soul.exists():
        soul.parent.mkdir(parents=True, exist_ok=True)
        soul.write_text("# Hermes Forge Bootstrap Coordinator\n\nCoordinate adaptive onboarding and report only observed status.\n", encoding="utf-8")
    status = "completed" if len(profiles) == size and not errors and all(p["verified"] for p in profiles) else "partial"
    write_state(status, config, profiles, errors)
    print(f"Status: {status}")
    print(f"State: {STATE_FILE}")
    return 0 if status == "completed" else 1

if __name__ == "__main__":
    raise SystemExit(main())
