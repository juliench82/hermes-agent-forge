from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
QUESTION = "What do you want to accomplish with Hermes?"


class HermesActivationTests(unittest.TestCase):
    def test_hermes_md_is_the_activation_entrypoint(self):
        content = (ROOT / "HERMES.md").read_text(encoding="utf-8")
        self.assertIn(QUESTION, content)
        self.assertLess(content.index(QUESTION), 400)
        self.assertIn("Do not summarize the architecture.", content)
        self.assertIn("Do not run install.sh.", content)
        self.assertIn("Do not treat profiles/ as the customer team.", content)
        self.assertNotIn("BOOTSTRAP.md", content)

    def test_readme_repeats_the_first_question(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(QUESTION, content)
        self.assertLess(content.index(QUESTION), 400)
        self.assertIn("HERMES.md", content)

    def test_root_does_not_keep_parallel_activation_files(self):
        self.assertFalse((ROOT / "BOOTSTRAP.md").exists())
        self.assertFalse((ROOT / "bootstrap.activation.json").exists())


if __name__ == "__main__":
    unittest.main()
