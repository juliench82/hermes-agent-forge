from pathlib import Path
import json
import unittest


ROOT = Path(__file__).parents[1]


class BootstrapActivationTests(unittest.TestCase):
    def test_hermes_context_file_starts_onboarding(self):
        content = (ROOT / "HERMES.md").read_text(encoding="utf-8")
        self.assertIn("What do you want to accomplish with Hermes?", content)
        self.assertIn("Do not summarize the architecture.", content)
        self.assertIn("Do not run install.sh.", content)
        self.assertIn("Do not treat profiles/ as the customer team.", content)

    def test_bootstrap_and_readme_use_the_same_first_question(self):
        question = "What do you want to accomplish with Hermes?"
        for name in ("BOOTSTRAP.md", "README.md"):
            with self.subTest(name=name):
                content = (ROOT / name).read_text(encoding="utf-8")
                self.assertIn(question, content)
                self.assertLess(content.index(question), 400)

    def test_activation_contract_is_immediate_and_dynamic(self):
        payload = json.loads((ROOT / "bootstrap.activation.json").read_text(encoding="utf-8"))
        activation = payload["activation"]
        self.assertEqual(activation["mode"], "immediate_onboarding")
        self.assertEqual(activation["customer_profiles"], "dynamic")
        self.assertEqual(
            activation["first_user_message"],
            "What do you want to accomplish with Hermes?",
        )
        self.assertIn("architecture_tour", activation["forbidden_first_actions"])
        self.assertIn("install.sh", activation["forbidden_first_actions"])


if __name__ == "__main__":
    unittest.main()
