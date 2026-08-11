"""
test_clean_install.py — E2E clean-install tests for hermes-agent-forge.
"""

import json
import hashlib
from pathlib import Path

# Import from the installer script
from scripts.hermes_forge_install import load_bootstrap_manifest, sha256_file, DEFAULT_PROFILES


def test_bootstrap_manifest_schema():
    """Verify bootstrap.manifest.json conforms to expected schema."""
    manifest, manifest_path = load_bootstrap_manifest()
    assert manifest["schema_version"] == "bootstrap-manifest.v1"
    assert manifest["repo_kind"] == "bootstrap"
    assert "default_team" in manifest
    assert "installer_entrypoint" in manifest
    assert manifest.get("config_onboarding_required") == True


def test_bootstrap_manifest_hash_stable():
    """Verify bootstrap manifest hash is stable across multiple computations."""
    manifest, manifest_path = load_bootstrap_manifest()
    hash1 = sha256_file(manifest_path)
    hash2 = sha256_file(manifest_path)
    assert hash1 == hash2
    # Also verify it's a valid SHA256 hex string (64 chars)
    assert len(hash1) == 64
    assert all(c in "0123456789abcdef" for c in hash1)


def test_default_profiles():
    """Verify default team profiles list."""
    assert len(DEFAULT_PROFILES) == 5
    assert "orchestrator" in DEFAULT_PROFILES
    assert "product-strategist" in DEFAULT_PROFILES
    assert "architect" in DEFAULT_PROFILES
    assert "builder" in DEFAULT_PROFILES
    assert "quality-guardian" in DEFAULT_PROFILES


def test_manifest_installer_entrypoint_exists():
    """Verify the installer entrypoint file exists."""
    manifest, _ = load_bootstrap_manifest()
    entrypoint = Path(manifest["installer_entrypoint"])
    assert entrypoint.exists(), f"Installer entrypoint {entrypoint} does not exist"


def test_state_directory_outside_repo():
    """Verify state directory is outside the bootstrap repo."""
    manifest, _ = load_bootstrap_manifest()
    state_dir = manifest.get("state_directory", "~/.hermes-forge/")
    assert state_dir.startswith("~/.hermes-forge/"), f"State directory {state_dir} is not outside the repo"
