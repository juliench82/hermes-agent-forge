from pathlib import Path

import pytest

from runtime.role_assets import RoleAssetError, RoleAssetInstaller

def test_installs_only_explicit_mappings_and_returns_hashes(tmp_path):
    source = tmp_path / "role"
    profile = tmp_path / "profile"
    source.mkdir()
    (source / "skill.md").write_text("role skill", encoding="utf-8")
    installed = RoleAssetInstaller().install(source, profile, {"skill.md": "skills/agent-forge-role.md"})
    assert (profile / "skills/agent-forge-role.md").read_text(encoding="utf-8") == "role skill"
    assert len(installed[0].sha256) == 64

def test_rejects_missing_or_escaping_assets(tmp_path):
    source = tmp_path / "role"
    source.mkdir()
    with pytest.raises(RoleAssetError):
        RoleAssetInstaller().install(source, tmp_path / "profile", {"missing.md": "skills/x.md"})
    (source / "skill.md").write_text("x", encoding="utf-8")
    with pytest.raises(RoleAssetError):
        RoleAssetInstaller().install(source, tmp_path / "profile", {"skill.md": "../escape.md"})

def test_identical_rerun_is_idempotent(tmp_path):
    source = tmp_path / "role"
    profile = tmp_path / "profile"
    source.mkdir()
    (source / "skill.md").write_text("stable", encoding="utf-8")
    installer = RoleAssetInstaller()
    first = installer.install(source, profile, {"skill.md": "skill.md"})
    second = installer.install(source, profile, {"skill.md": "skill.md"})
    assert first == second
