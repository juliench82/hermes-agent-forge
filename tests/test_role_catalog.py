"""Tests for the use-case role catalog."""
import unittest
from compiler.role_catalog import (
    RoleCatalogError,
    get_profiles,
    get_role_description,
    get_use_case_description,
    list_use_cases,
    validate_profiles,
)


class RoleCatalogTests(unittest.TestCase):
    def test_list_use_cases_returns_sorted_ids(self):
        use_cases = list_use_cases()
        self.assertEqual(use_cases, sorted(use_cases))
        self.assertIn("solo-founder-saas", use_cases)
        self.assertIn("music-band-promotion", use_cases)
        self.assertIn("e-commerce-support", use_cases)

    def test_get_profiles_returns_correct_3_profile_team_for_solo_founder(self):
        profiles = get_profiles("solo-founder-saas", 3)
        self.assertEqual(profiles, ["orchestrator", "builder", "quality-guardian"])

    def test_get_profiles_returns_correct_5_profile_team_for_solo_founder(self):
        profiles = get_profiles("solo-founder-saas", 5)
        self.assertEqual(profiles, ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"])

    def test_get_profiles_returns_correct_7_profile_team_for_solo_founder(self):
        profiles = get_profiles("solo-founder-saas", 7)
        self.assertEqual(profiles, ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian", "self-improver", "devops-security"])

    def test_get_profiles_returns_correct_3_profile_team_for_music_band(self):
        profiles = get_profiles("music-band-promotion", 3)
        self.assertEqual(profiles, ["orchestrator", "social-media-manager", "content-creator"])

    def test_get_profiles_returns_correct_5_profile_team_for_music_band(self):
        profiles = get_profiles("music-band-promotion", 5)
        self.assertEqual(profiles, ["orchestrator", "marketing-lead", "social-media-manager", "content-creator", "booking-agent"])

    def test_get_profiles_returns_correct_7_profile_team_for_music_band(self):
        profiles = get_profiles("music-band-promotion", 7)
        self.assertEqual(profiles, ["orchestrator", "marketing-lead", "social-media-manager", "content-creator", "booking-agent", "merch-manager", "self-improver"])

    def test_get_profiles_returns_correct_3_profile_team_for_ecommerce(self):
        profiles = get_profiles("e-commerce-support", 3)
        self.assertEqual(profiles, ["orchestrator", "support-agent", "order-manager"])

    def test_get_profiles_returns_correct_5_profile_team_for_ecommerce(self):
        profiles = get_profiles("e-commerce-support", 5)
        self.assertEqual(profiles, ["orchestrator", "product-strategist", "support-agent", "order-manager", "quality-guardian"])

    def test_get_profiles_returns_correct_7_profile_team_for_ecommerce(self):
        profiles = get_profiles("e-commerce-support", 7)
        self.assertEqual(profiles, ["orchestrator", "product-strategist", "architect", "support-agent", "order-manager", "quality-guardian", "devops-security"])

    def test_get_profiles_raises_for_unknown_use_case(self):
        with self.assertRaisesRegex(RoleCatalogError, "unsupported use case"):
            get_profiles("unknown-use-case", 5)

    def test_get_profiles_raises_for_invalid_team_size(self):
        with self.assertRaisesRegex(RoleCatalogError, "unsupported team size"):
            get_profiles("solo-founder-saas", 4)
        with self.assertRaisesRegex(RoleCatalogError, "unsupported team size"):
            get_profiles("solo-founder-saas", 6)

    def test_get_role_description_returns_description(self):
        desc = get_role_description("orchestrator")
        self.assertIn("Coordinate", desc)

    def test_get_use_case_description_returns_description(self):
        desc = get_use_case_description("music-band-promotion")
        self.assertIn("Musician", desc)

    def test_validate_profiles_accepts_valid_list(self):
        validate_profiles(["orchestrator", "builder"])

    def test_validate_profiles_rejects_empty_list(self):
        with self.assertRaisesRegex(RoleCatalogError, "cannot be empty"):
            validate_profiles([])

    def test_validate_profiles_rejects_more_than_7(self):
        with self.assertRaisesRegex(RoleCatalogError, "exceeds maximum of 7"):
            validate_profiles(["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"])

    def test_validate_profiles_rejects_invalid_id(self):
        with self.assertRaisesRegex(RoleCatalogError, "invalid profile ID"):
            validate_profiles(["orchestrator", ""])


if __name__ == "__main__":
    unittest.main()
