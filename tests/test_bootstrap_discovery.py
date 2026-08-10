"""Sprint 4: bootstrap discovery contract validation."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

from compiler.bootstrap_discovery import (
    BootstrapDiscoveryError,
    DEFAULT_DISCOVERY_ORDER,
    discover_bootstrap,
    is_bootstrap_repository,
    load_bootstrap_manifest,
    validate_bootstrap_manifest,
    validate_referenced_paths,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "bootstrap.manifest.json"
SCHEMA_PATH = ROOT / "schemas" / "bootstrap-manifest.v1.schema.json"


class BootstrapManifestPresenceTests(unittest.TestCase):
    def test_bootstrap_manifest_exists(self) -> None:
        self.assertTrue(MANIFEST_PATH.is_file(), "bootstrap.manifest.json must exist at repo root")

    def test_bootstrap_schema_exists(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file(), "bootstrap-manifest.v1.schema.json must exist")

    def test_canonical_entrypoint_exists(self) -> None:
        self.assertTrue((ROOT / "BOOTSTRAP.md").is_file())


class BootstrapDiscoveryHappyPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = discover_bootstrap(ROOT)

    def test_manifest_identifies_bootstrap_source(self) -> None:
        self.assertEqual(self.result.source_type, "hermes-bootstrap")
        self.assertTrue(self.result.is_bootstrap_source)
        self.assertFalse(self.result.user_project_repository)

    def test_manifest_references_canonical_entrypoint(self) -> None:
        self.assertEqual(self.result.entrypoint, "BOOTSTRAP.md")

    def test_discovery_order_matches_contract(self) -> None:
        # Required prefixes from the product contract; machine-readable manifest may
        # appear immediately after BOOTSTRAP.md.
        order = self.result.discovery_order
        self.assertEqual(order[0], "BOOTSTRAP.md")
        self.assertIn("README.md", order)
        self.assertIn("onboarding/", order)
        self.assertIn("profiles/", order)
        self.assertIn("schemas/", order)
        self.assertIn("catalog/", order)
        self.assertIn("packs/", order)
        self.assertIn("examples/", order)
        self.assertIn("runtime/", order)
        self.assertIn("tests/", order)
        # Preserve relative order of the conceptual product contract paths.
        conceptual = [p for p in DEFAULT_DISCOVERY_ORDER if p != "bootstrap.manifest.json"]
        positions = [order.index(p) for p in conceptual if p in order]
        self.assertEqual(positions, sorted(positions))

    def test_all_discovery_paths_exist(self) -> None:
        validate_referenced_paths(ROOT, self.result.manifest)

    def test_onboarding_entrypoints_exist(self) -> None:
        self.assertIn("onboarding/START.md", self.result.onboarding_entrypoints)
        self.assertIn("onboarding/manifest.md", self.result.onboarding_entrypoints)
        for relative in self.result.onboarding_entrypoints:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_required_profiles_are_discoverable(self) -> None:
        expected = [
            "orchestrator",
            "product-strategist",
            "architect",
            "builder",
            "quality-guardian",
        ]
        self.assertEqual(self.result.required_profiles, expected)
        self.assertEqual(self.result.default_enabled_profiles, expected)
        for profile_id in expected:
            self.assertTrue((ROOT / "profiles" / profile_id).is_dir(), profile_id)

    def test_optional_self_improver_not_default_enabled(self) -> None:
        self.assertIn("self-improver", self.result.optional_profiles)
        self.assertNotIn("self-improver", self.result.default_enabled_profiles)

    def test_required_schemas_are_present(self) -> None:
        for relative in self.result.required_schemas:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_at_least_one_use_case_example_exists(self) -> None:
        self.assertGreaterEqual(len(self.result.required_examples), 1)
        for relative in self.result.required_examples:
            self.assertTrue((ROOT / relative).is_file(), relative)
        self.assertTrue(
            (ROOT / "examples" / "solo-founder-app-builder.tenant-spec.json").is_file()
        )

    def test_is_bootstrap_repository_helper(self) -> None:
        self.assertTrue(is_bootstrap_repository(ROOT))

    def test_sprint4_capabilities_do_not_provision(self) -> None:
        caps = self.result.capabilities
        self.assertTrue(caps.get("recogniseBootstrapSource", True))
        self.assertFalse(caps.get("provisionTeam", False))
        self.assertFalse(caps.get("connectUserProjectRepository", False))
        self.assertEqual(self.result.next_step, "onboarding")


class BootstrapDiscoveryFailureTests(unittest.TestCase):
    def _clone_repo_subset(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="haf-bootstrap-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        # Minimal tree sufficient for positive validation before mutations.
        for relative in [
            "BOOTSTRAP.md",
            "bootstrap.manifest.json",
            "README.md",
            "onboarding/START.md",
            "onboarding/manifest.md",
            "schemas/bootstrap-manifest.v1.schema.json",
            "schemas/hermes-bundle.v1.schema.json",
            "schemas/tenant-spec.v1.schema.json",
            "examples/solo-founder-app-builder.tenant-spec.json",
        ]:
            src = ROOT / relative
            dst = tmp / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():
                shutil.copy2(src, dst)
            else:
                dst.write_text("# fixture\n", encoding="utf-8")
        for profile_id in [
            "orchestrator",
            "product-strategist",
            "architect",
            "builder",
            "quality-guardian",
        ]:
            (tmp / "profiles" / profile_id).mkdir(parents=True, exist_ok=True)
        for directory in ["catalog", "packs", "runtime", "tests", "onboarding", "examples", "schemas", "profiles"]:
            (tmp / directory).mkdir(parents=True, exist_ok=True)
        # Ensure directories listed in discovery order exist even if empty.
        return tmp

    def _write_manifest(self, root: Path, manifest: Dict[str, Any]) -> None:
        (root / "bootstrap.manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_missing_manifest_fails(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="haf-empty-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        with self.assertRaisesRegex(BootstrapDiscoveryError, "bootstrap manifest not found"):
            load_bootstrap_manifest(tmp)

    def test_invalid_source_type_is_rejected(self) -> None:
        tmp = self._clone_repo_subset()
        manifest = json.loads((tmp / "bootstrap.manifest.json").read_text(encoding="utf-8"))
        manifest["sourceType"] = "user-application"
        self._write_manifest(tmp, manifest)
        with self.assertRaisesRegex(BootstrapDiscoveryError, "sourceType"):
            validate_bootstrap_manifest(manifest)

    def test_missing_referenced_path_fails_with_actionable_error(self) -> None:
        tmp = self._clone_repo_subset()
        manifest = json.loads((tmp / "bootstrap.manifest.json").read_text(encoding="utf-8"))
        target = tmp / "onboarding" / "START.md"
        target.unlink()
        with self.assertRaisesRegex(BootstrapDiscoveryError, "required file missing: onboarding/START.md"):
            validate_referenced_paths(tmp, manifest)

    def test_missing_required_profile_fails(self) -> None:
        tmp = self._clone_repo_subset()
        manifest = json.loads((tmp / "bootstrap.manifest.json").read_text(encoding="utf-8"))
        shutil.rmtree(tmp / "profiles" / "builder")
        with self.assertRaisesRegex(BootstrapDiscoveryError, "required profile not discoverable: profiles/builder"):
            validate_referenced_paths(tmp, manifest)

    def test_discovery_is_read_only(self) -> None:
        tmp = self._clone_repo_subset()
        before = {
            path.relative_to(tmp).as_posix(): path.stat().st_mtime_ns
            for path in tmp.rglob("*")
            if path.is_file()
        }
        discover_bootstrap(tmp)
        after = {
            path.relative_to(tmp).as_posix(): path.stat().st_mtime_ns
            for path in tmp.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_provision_capability_true_is_rejected(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["capabilities"] = dict(manifest.get("capabilities") or {})
        manifest["capabilities"]["provisionTeam"] = True
        with self.assertRaisesRegex(BootstrapDiscoveryError, "provisionTeam"):
            validate_bootstrap_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
