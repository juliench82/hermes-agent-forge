"""Bootstrap repository discovery and validation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

CANONICAL_ENTRYPOINT = "HERMES.md"

DEFAULT_DISCOVERY_ORDER = [
    "HERMES.md",
    "bootstrap.manifest.json",
    "README.md",
    "onboarding/",
    "profiles/",
    "schemas/",
    "catalog/",
    "packs/",
    "examples/",
    "runtime/",
    "tests/",
]


class BootstrapDiscoveryError(Exception):
    """Raised when bootstrap discovery validation fails."""


class BootstrapDiscoveryResult(NamedTuple):
    """Result of successful bootstrap discovery."""

    is_bootstrap_source: bool
    source_type: str
    entrypoint: str
    discovery_order: List[str]
    manifest: Dict[str, Any]
    onboarding_entrypoints: List[str]
    required_profiles: List[str]
    default_enabled_profiles: List[str]
    optional_profiles: List[str]
    required_schemas: List[str]
    required_examples: List[str]
    capabilities: Dict[str, bool]
    next_step: str
    user_project_repository: bool


def load_bootstrap_manifest(root: Path) -> Dict[str, Any]:
    """Load and return the bootstrap manifest from the repository root."""
    manifest_path = root / "bootstrap.manifest.json"
    if not manifest_path.is_file():
        raise BootstrapDiscoveryError("bootstrap manifest not found at bootstrap.manifest.json")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def validate_bootstrap_manifest(manifest: Dict[str, Any]) -> None:
    """Validate the bootstrap manifest structure and constraints."""
    if manifest.get("sourceType") != "hermes-bootstrap":
        raise BootstrapDiscoveryError("sourceType must be 'hermes-bootstrap'")
    
    entrypoint = manifest.get("entrypoint")
    if entrypoint != CANONICAL_ENTRYPOINT:
        raise BootstrapDiscoveryError(f"entrypoint must be '{CANONICAL_ENTRYPOINT}'")
    
    caps = manifest.get("capabilities", {})
    if caps.get("provisionTeam", False):
        raise BootstrapDiscoveryError("capabilities.provisionTeam must be false during discovery")
    if caps.get("connectUserProjectRepository", False):
        raise BootstrapDiscoveryError("capabilities.connectUserProjectRepository must be false during discovery")


def validate_referenced_paths(root: Path, manifest: Dict[str, Any]) -> None:
    """Validate that all paths referenced in the manifest exist."""
    entrypoint_path = root / manifest.get("entrypoint", "")
    if not entrypoint_path.is_file():
        raise BootstrapDiscoveryError(f"required file missing: {manifest.get('entrypoint')}")
    
    manifest_path = root / "bootstrap.manifest.json"
    if not manifest_path.is_file():
        raise BootstrapDiscoveryError("required file missing: bootstrap.manifest.json")
    
    discovery_order = manifest.get("discoveryOrder", [])
    for relative_path in discovery_order:
        full_path = root / relative_path
        if not full_path.exists():
            raise BootstrapDiscoveryError(f"required path missing: {relative_path}")
    
    onboarding_dir = root / "onboarding"
    if onboarding_dir.is_dir():
        for entry in ["START.md", "manifest.md"]:
            if not (onboarding_dir / entry).is_file():
                raise BootstrapDiscoveryError(f"required file missing: onboarding/{entry}")
    
    profiles_dir = root / "profiles"
    if profiles_dir.is_dir():
        required_profiles = manifest.get("profiles", {}).get("required", [])
        for profile_id in required_profiles:
            if not (profiles_dir / profile_id).is_dir():
                raise BootstrapDiscoveryError(f"required profile not discoverable: profiles/{profile_id}")


def discover_bootstrap(root: Path) -> BootstrapDiscoveryResult:
    """Discover and validate a bootstrap repository."""
    manifest = load_bootstrap_manifest(root)
    validate_bootstrap_manifest(manifest)
    validate_referenced_paths(root, manifest)
    
    entrypoint = manifest.get("entrypoint", CANONICAL_ENTRYPOINT)
    discovery_order = manifest.get("discoveryOrder", DEFAULT_DISCOVERY_ORDER)
    
    onboarding_entrypoints = []
    onboarding_dir = root / "onboarding"
    if onboarding_dir.is_dir():
        for entry in onboarding_dir.iterdir():
            if entry.is_file() and entry.suffix == ".md":
                onboarding_entrypoints.append(f"onboarding/{entry.name}")
    
    profiles_config = manifest.get("profiles", {})
    required_profiles = profiles_config.get("required", [])
    default_enabled = profiles_config.get("defaultEnabled", required_profiles)
    optional_profiles = profiles_config.get("optional", [])
    
    required_schemas = []
    schemas_dir = root / "schemas"
    if schemas_dir.is_dir():
        for entry in schemas_dir.iterdir():
            if entry.is_file() and entry.suffix == ".json":
                required_schemas.append(f"schemas/{entry.name}")
    
    required_examples = []
    examples_dir = root / "examples"
    if examples_dir.is_dir():
        for entry in examples_dir.iterdir():
            if entry.is_file() and entry.suffix == ".json":
                required_examples.append(f"examples/{entry.name}")
    
    capabilities = manifest.get("capabilities", {})
    next_step = manifest.get("nextStep", "onboarding")
    user_project_repo = manifest.get("userProjectRepository", False)
    
    return BootstrapDiscoveryResult(
        is_bootstrap_source=True,
        source_type=manifest.get("sourceType", "hermes-bootstrap"),
        entrypoint=entrypoint,
        discovery_order=discovery_order,
        manifest=manifest,
        onboarding_entrypoints=onboarding_entrypoints,
        required_profiles=required_profiles,
        default_enabled_profiles=default_enabled,
        optional_profiles=optional_profiles,
        required_schemas=required_schemas,
        required_examples=required_examples,
        capabilities=capabilities,
        next_step=next_step,
        user_project_repository=user_project_repo,
    )


def is_bootstrap_repository(root: Path) -> bool:
    """Check if a repository is a valid bootstrap source."""
    try:
        discover_bootstrap(root)
        return True
    except BootstrapDiscoveryError:
        return False
