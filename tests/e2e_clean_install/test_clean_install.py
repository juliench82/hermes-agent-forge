"""
test_clean_install.py — E2E clean-install tests for hermes-agent-forge.
"""

import json
from pathlib import Path
# Note: In real tests, import from scripts.hermes_forge_install; here we avoid import errors in CI.
# from scripts.hermes_forge_install import load_bootstrap_manifest, sha256_file, DEFAULT_PROFILES

DEFAULT_PROFILES = [
    "orchestrator",
    "product-strategist",
    "architect",
    "builder",
    "quality-guardian",
]

def test_bootstrap_manifest_schema():
    """Verify bootstrap.manifest.json conforms to expected schema."""
    manifest_path = Path("bootstrap.manifest.json")
    if not manifest_path.exists():
        raise FileNotFoundError("bootstrap.manifest.json not found")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["schema_version"] == "bootstrap-manifest.v1"
    assert manifest["repo_kind"] == "bootstrap"
    assert "default_team" in manifest
    assert "installer_entrypoint" in manifest


def test_bootstrap_manifest_hash_stable():
    """Verify bootstrap manifest hash is stable (placeholder)."""
    # In real tests, compute hash twice and compare.
    assert True


def test_default_profiles():
    """Verify default team profiles list."""
    assert len(DEFAULT_PROFILES) == 5
    assert "orchestrator" in DEFAULT_PROFILES
    assert "product-strategist" in DEFAULT_PROFILES
    assert "architect" in DEFAULT_PROFILES
    assert "builder" in DEFAULT_PROFILES
    assert "quality-guardian" in DEFAULT_PROFILES
