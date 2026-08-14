import unittest

from runtime.evidence_skill_verification import (
    EvidenceBasedSkillVerifier,
    ResolutionSource,
    SkillVerificationError,
)


class EvidenceBasedSkillVerifierTests(unittest.TestCase):
    def setUp(self):
        self.verifier = EvidenceBasedSkillVerifier()

    def test_accepts_one_to_ten_unique_capabilities(self):
        self.assertEqual(self.verifier.validate_capabilities(["testing"]), ("testing",))
        self.assertEqual(len(self.verifier.validate_capabilities([str(i) for i in range(10)])), 10)

    def test_rejects_invalid_capability_cardinality(self):
        for capabilities in ([], [str(i) for i in range(11)], ["testing", "testing"], [""]):
            with self.subTest(capabilities=capabilities):
                with self.assertRaises(SkillVerificationError):
                    self.verifier.validate_capabilities(capabilities)

    def test_resolves_exact_observed_identity_and_source(self):
        resolution = self.verifier.resolve(
            "testing",
            observed_candidates={"pytest-runner": ResolutionSource.LOCAL},
            search_evidence="observed local skill listing",
        )
        self.assertEqual(resolution.selected_identity, "pytest-runner")
        self.assertEqual(resolution.resolution_source, ResolutionSource.LOCAL)
        self.assertEqual(resolution.status, "proposed")

    def test_rejects_missing_or_ambiguous_evidence(self):
        with self.assertRaises(SkillVerificationError):
            self.verifier.resolve("testing", observed_candidates={}, search_evidence="listing")
        with self.assertRaises(SkillVerificationError):
            self.verifier.resolve(
                "testing",
                observed_candidates={
                    "pytest-runner": ResolutionSource.LOCAL,
                    "other-runner": ResolutionSource.CATALOG,
                },
                search_evidence="listing",
            )
        with self.assertRaises(SkillVerificationError):
            self.verifier.resolve(
                "testing",
                observed_candidates={"pytest-runner": ResolutionSource.LOCAL},
                search_evidence="",
            )

    def test_requires_post_install_observation(self):
        resolution = self.verifier.resolve(
            "testing",
            observed_candidates={"pytest-runner": ResolutionSource.LOCAL},
            search_evidence="listing",
        )
        verified = self.verifier.verify_installed(
            resolution,
            ["pytest-runner"],
            "observed installed-skill listing",
        )
        self.assertEqual(verified.status, "verified")
        self.assertEqual(verified.verification_evidence, "observed installed-skill listing")
        with self.assertRaises(SkillVerificationError):
            self.verifier.verify_installed(resolution, ["other"], "listing")


if __name__ == "__main__":
    unittest.main()
