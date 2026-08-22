"""Legacy Hermes adapter tests — DEPRECATED.

These tests reference the removed profiles/ directory structure.
The functionality is now covered by:
- tests/test_dynamic_profiles.py
- tests/test_profile_assets.py
- tests/test_main_profile_assets.py

See: commit a8e14a1 ("cleanup: remove hardcoded profiles directory")
"""
import unittest


class HermesAdapterTests(unittest.TestCase):
    """Legacy adapter tests — all skipped."""

    @unittest.skip(
        "Legacy adapter tests - profiles/ directory removed in favor of dynamic generation. "
        "Use test_dynamic_profiles.py and test_profile_assets.py instead. "
        "See: commit a8e14a1"
    )
    def test_compatibility_spec_validates_and_preserves_legacy_profiles(self):
        """Skipped - legacy test."""
        pass

    @unittest.skip(
        "Legacy adapter tests - profiles/ directory removed in favor of dynamic generation. "
        "Use test_dynamic_profiles.py and test_profile_assets.py instead. "
        "See: commit a8e14a1"
    )
    def test_contract_version_and_status(self):
        """Skipped - legacy test."""
        pass

    @unittest.skip(
        "Legacy adapter tests - profiles/ directory removed in favor of dynamic generation. "
        "Use test_dynamic_profiles.py and test_profile_assets.py instead. "
        "See: commit a8e14a1"
    )
    def test_delegation_and_handoff_structure(self):
        """Skipped - legacy test."""
        pass

    @unittest.skip(
        "Legacy adapter tests - profiles/ directory removed in favor of dynamic generation. "
        "Use test_dynamic_profiles.py and test_profile_assets.py instead. "
        "See: commit a8e14a1"
    )
    def test_profile_identity_version_skills_io_routing_approval_namespace(self):
        """Skipped - legacy test."""
        pass

    @unittest.skip(
        "Legacy adapter tests - profiles/ directory removed in favor of dynamic generation. "
        "Use test_dynamic_profiles.py and test_profile_assets.py instead. "
        "See: commit a8e14a1"
    )
    def test_render_is_deterministic(self):
        """Skipped - legacy test."""
        pass

    @unittest.skip(
        "Legacy adapter tests - profiles/ directory removed in favor of dynamic generation. "
        "Use test_dynamic_profiles.py and test_profile_assets.py instead. "
        "See: commit a8e14a1"
    )
    def test_stage_agent_mapping(self):
        """Skipped - legacy test."""
        pass


if __name__ == "__main__":
    unittest.main()
