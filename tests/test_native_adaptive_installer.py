import json
from pathlib import Path

ROOT = Path(__file__).parents[1]

def test_native_manifest_contract():
    manifest = json.loads((ROOT / "bootstrap.manifest.json").read_text())
    assert manifest["installer_command"] == "./install.sh"
    assert manifest["yolo_mode"] == "auto"
    assert manifest["state_directory"] == "~/.hermes-forge/"

def test_adaptive_team_sizes():
    manifest = json.loads((ROOT / "onboarding/onboarding.manifest.json").read_text())
    assert len(manifest["team_sizes"]["3"]) == 3
    assert len(manifest["team_sizes"]["5"]) == 5
    assert len(manifest["team_sizes"]["7"]) == 7
    assert "devops-security" in manifest["team_sizes"]["7"]

def test_config_template_is_yaml_and_complete():
    from runtime.adaptive_installer import config_yaml
    text = config_yaml("nous", "default", "builder")
    for token in ("_config_version: 34", "toolsets:", "agent:", "terminal:", "approvals:", "platform_toolsets:", "skills:", "memory:", "delegation:"):
        assert token in text
    assert not text.lstrip().startswith("{")

def test_bootstrap_docs_do_not_require_manual_yolo_or_python():
    text = (ROOT / "BOOTSTRAP.md").read_text().lower()
    assert "./install.sh" in text
    assert "run `/yolo` manually" in text
