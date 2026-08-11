import unittest

from runtime.bootstrap_controller import (
    BOOTSTRAP_CONTROLLER_PROFILE_NAMES,
    BootstrapContractError,
    BootstrapControllerContract,
    approval_matches,
    canonical_plan_hash,
)


class BootstrapControllerContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = BootstrapControllerContract()

    def test_default_and_main_are_reserved_for_controller(self):
        self.assertEqual(BOOTSTRAP_CONTROLLER_PROFILE_NAMES, {"default", "main"})
        with self.assertRaises(BootstrapContractError):
            self.contract.validate_customer_profile_names(["default"])
        with self.assertRaises(BootstrapContractError):
            self.contract.validate_customer_profile_names(["main"])

    def test_customer_names_remain_dynamic(self):
        self.assertEqual(
            self.contract.validate_customer_profile_names(["researcher", "builder"]),
            ("researcher", "builder"),
        )

    def test_customer_names_are_unique_and_non_empty(self):
        for names in (("builder", "builder"), (" ",), ("builder", "")):
            with self.subTest(names=names):
                with self.assertRaises(BootstrapContractError):
                    self.contract.validate_customer_profile_names(names)

    def test_plan_hash_is_canonical(self):
        first = {"profiles": ["builder"], "approval": True}
        second = {"approval": True, "profiles": ["builder"]}
        self.assertEqual(canonical_plan_hash(first), canonical_plan_hash(second))
        self.assertNotEqual(canonical_plan_hash(first), canonical_plan_hash({"profiles": ["reviewer"]}))

    def test_approval_is_bound_to_exact_plan(self):
        plan = {"profiles": ["builder"], "skills": {"builder": ["testing"]}}
        approved = canonical_plan_hash(plan)
        self.assertTrue(approval_matches(plan, approved))
        self.assertFalse(approval_matches({"profiles": ["builder"], "skills": {}}, approved))

    def test_live_provisioning_is_rejected(self):
        with self.assertRaises(BootstrapContractError):
            BootstrapControllerContract(live_provisioning=True)


if __name__ == "__main__":
    unittest.main()
