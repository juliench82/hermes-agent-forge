"""Read-only bootstrap discovery for Hermes Agent Forge.

Sprint 4: recognise this repository as a hermes-bootstrap source.
Does not start onboarding, provision teams, or connect user project repos.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

MANIFEST_FILENAME = "bootstrap.manifest.json"
CANONICAL_ENTRYPOINT = "BOOTSTRAP.md"
SOURCE_TYPE = "hermes-bootstrap"
API_VERSION = "hermes.bootstrap/v1"
KIND = "BootstrapManifest"

DEFAULT_DISCOVERY_ORDER: List[str] = [
    "BOOTSTRAP.md",
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


class BootstrapDiscoveryError(ValueError):
    """Raised when bootstrap discovery or validation fails."""


@dataclass(frozen=True)
class BootstrapDiscovery:
    """Structured result of a successful bootstrap discovery."""

    root: Path
    source_type: str
    name: str
    entrypoint: str
    discovery_order: List[str]
    onboarding_entrypoints: List[str]
    required_profiles: List[str]
    default_enabled_profiles: List[str]
    optional_profiles: List[str]
    required_schemas: List[str]
    required_examples: List[str]
    capabilities: Dict[str, bool]
    next_step: str
    manifest: Dict[str, Any] = field(repr=False)
    user_project_repository: bool = False

    @property
    def is_bootstrap_source(self) -> bool:
        return self.source_type == SOURCE_TYPE and not self.user_project_repository


def _fail(message: str) -> None:
    raise BootstrapDiscoveryError(message)


def _as_list(value: Any, path: str) -> List[Any]:
    if not isinstance(value, list) or not value:
        _fail(f"{path}: expected a non-empty list")
    return value


def _as_str_list(value: Any, path: str) -> List[str]:
    items = _as_list(value, path)
    result: List[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, str) or not item.strip():
            _fail(f"{path}[{index}]: expected a non-empty string")
        result.append(item)
    return result


def _require_keys(data: Dict[str, Any], keys: Sequence[str], path: str = "$") -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        _fail(f"{path}: missing required fields: {sorted(missing)}")


def load_bootstrap_manifest(root: Path | str) -> Dict[str, Any]:
    """Load bootstrap.manifest.json from a repository root."""
    root_path = Path(root).resolve()
    manifest_path = root_path / MANIFEST_FILENAME
    if not manifest_path.is_file():
        _fail(f"bootstrap manifest not found: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail(f"invalid JSON in {manifest_path}: {exc}")
    if not isinstance(data, dict):
        _fail(f"{manifest_path}: root value must be an object")
    return data


def validate_bootstrap_manifest(manifest: Dict[str, Any]) -> None:
    """Validate the semantic bootstrap-manifest contract (pure Python)."""
    _require_keys(
        manifest,
        [
            "apiVersion",
            "kind",
            "manifestVersion",
            "sourceType",
            "name",
            "entrypoint",
            "discoveryOrder",
            "onboarding",
            "profiles",
            "schemas",
            "examples",
        ],
    )
    if manifest.get("apiVersion") != API_VERSION:
        _fail(f"unsupported apiVersion: {manifest.get('apiVersion')!r}")
    if manifest.get("kind") != KIND:
        _fail(f"unsupported kind: {manifest.get('kind')!r}")
    if manifest.get("sourceType") != SOURCE_TYPE:
        _fail(f"sourceType must be {SOURCE_TYPE!r}")
    if manifest.get("entrypoint") != CANONICAL_ENTRYPOINT:
        _fail(f"entrypoint must be {CANONICAL_ENTRYPOINT!r}")

    repository = manifest.get("repository")
    if repository is not None:
        if not isinstance(repository, dict):
            _fail("repository: expected an object")
        if repository.get("role") != "bootstrap":
            _fail("repository.role must be 'bootstrap'")
        if repository.get("userProjectRepository") is not False:
            _fail("repository.userProjectRepository must be false")

    _as_str_list(manifest["discoveryOrder"], "discoveryOrder")

    onboarding = manifest["onboarding"]
    if not isinstance(onboarding, dict):
        _fail("onboarding: expected an object")
    _as_str_list(onboarding.get("entrypoints"), "onboarding.entrypoints")

    profiles = manifest["profiles"]
    if not isinstance(profiles, dict):
        _fail("profiles: expected an object")
    _require_keys(profiles, ["directory", "required", "defaultEnabled"], "profiles")
    _as_str_list(profiles["required"], "profiles.required")
    _as_str_list(profiles["defaultEnabled"], "profiles.defaultEnabled")
    if "optional" in profiles:
        optional = profiles["optional"]
        if not isinstance(optional, list):
            _fail("profiles.optional: expected a list")
        for index, item in enumerate(optional):
            if not isinstance(item, str) or not item.strip():
                _fail(f"profiles.optional[{index}]: expected a non-empty string")

    schemas = manifest["schemas"]
    if not isinstance(schemas, dict):
        _fail("schemas: expected an object")
    _require_keys(schemas, ["directory", "required"], "schemas")
    _as_str_list(schemas["required"], "schemas.required")

    examples = manifest["examples"]
    if not isinstance(examples, dict):
        _fail("examples: expected an object")
    _require_keys(examples, ["directory", "required"], "examples")
    _as_str_list(examples["required"], "examples.required")

    capabilities = manifest.get("capabilities") or {}
    if capabilities.get("provisionTeam") is True:
        _fail("capabilities.provisionTeam must not be true in Sprint 4 discovery")
    if capabilities.get("connectUserProjectRepository") is True:
        _fail("capabilities.connectUserProjectRepository must not be true for bootstrap source")


def _resolve_path(root: Path, relative: str) -> Path:
    rel = relative.rstrip("/")
    return root / rel


def _assert_path_exists(root: Path, relative: str, *, expect_dir: Optional[bool] = None) -> Path:
    path = _resolve_path(root, relative)
    if expect_dir is True:
        if not path.is_dir():
            _fail(f"required directory missing: {relative}")
    elif expect_dir is False:
        if not path.is_file():
            _fail(f"required file missing: {relative}")
    else:
        if relative.endswith("/"):
            if not path.is_dir():
                _fail(f"required directory missing: {relative}")
        elif not path.exists():
            _fail(f"required path missing: {relative}")
    return path


def validate_referenced_paths(root: Path | str, manifest: Dict[str, Any]) -> None:
    """Confirm every discovery path and required reference exists on disk."""
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        _fail(f"repository root is not a directory: {root_path}")

    _assert_path_exists(root_path, CANONICAL_ENTRYPOINT, expect_dir=False)
    _assert_path_exists(root_path, MANIFEST_FILENAME, expect_dir=False)

    for relative in _as_str_list(manifest["discoveryOrder"], "discoveryOrder"):
        _assert_path_exists(root_path, relative)

    onboarding = manifest["onboarding"]
    for relative in _as_str_list(onboarding["entrypoints"], "onboarding.entrypoints"):
        _assert_path_exists(root_path, relative, expect_dir=False)

    profiles = manifest["profiles"]
    profiles_dir = _assert_path_exists(root_path, profiles["directory"], expect_dir=True)
    for profile_id in _as_str_list(profiles["required"], "profiles.required"):
        profile_path = profiles_dir / profile_id
        if not profile_path.is_dir():
            _fail(f"required profile not discoverable: profiles/{profile_id}")

    for relative in _as_str_list(manifest["schemas"]["required"], "schemas.required"):
        _assert_path_exists(root_path, relative, expect_dir=False)

    for relative in _as_str_list(manifest["examples"]["required"], "examples.required"):
        _assert_path_exists(root_path, relative, expect_dir=False)

    examples_dir = manifest["examples"].get("directory")
    if examples_dir:
        _assert_path_exists(root_path, examples_dir, expect_dir=True)


def discover_bootstrap(root: Path | str) -> BootstrapDiscovery:
    """Discover and validate a Hermes bootstrap repository. Read-only."""
    root_path = Path(root).resolve()
    manifest = load_bootstrap_manifest(root_path)
    validate_bootstrap_manifest(manifest)
    validate_referenced_paths(root_path, manifest)

    onboarding = manifest["onboarding"]
    profiles = manifest["profiles"]
    schemas = manifest["schemas"]
    examples = manifest["examples"]
    repository = manifest.get("repository") or {}
    capabilities = dict(manifest.get("capabilities") or {})

    return BootstrapDiscovery(
        root=root_path,
        source_type=str(manifest["sourceType"]),
        name=str(manifest["name"]),
        entrypoint=str(manifest["entrypoint"]),
        discovery_order=list(manifest["discoveryOrder"]),
        onboarding_entrypoints=list(onboarding["entrypoints"]),
        required_profiles=list(profiles["required"]),
        default_enabled_profiles=list(profiles["defaultEnabled"]),
        optional_profiles=list(profiles.get("optional") or []),
        required_schemas=list(schemas["required"]),
        required_examples=list(examples["required"]),
        capabilities=capabilities,
        next_step=str(manifest.get("nextStep") or "onboarding"),
        manifest=manifest,
        user_project_repository=bool(repository.get("userProjectRepository", False)),
    )


def is_bootstrap_repository(root: Path | str) -> bool:
    """Return True when root contains a valid hermes-bootstrap manifest."""
    try:
        result = discover_bootstrap(root)
    except BootstrapDiscoveryError:
        return False
    return result.is_bootstrap_source
