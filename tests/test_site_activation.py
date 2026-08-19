from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).parents[1]
SITE = ROOT / "site"
SKILL_URL = "https://hermes-agents-forge.vercel.app/SKILL.md"
TERMINAL_COMMAND = f"hermes skills install {SKILL_URL} --name forge"
QUESTION = "What do you want Hermes to accomplish for you?"


class SiteActivationTests(unittest.TestCase):
    def test_canonical_skill_files_match(self):
        public = (SITE / "public" / "SKILL.md").read_text(encoding="utf-8")
        tap = (ROOT / "skills" / "forge" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(public, tap)

    def test_skill_frontmatter_is_valid(self):
        text = (SITE / "public" / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name: forge$")
        self.assertIn(QUESTION, text)
        self.assertIn("Never treat `/goal` as an alias", text)
        self.assertIn("Do not require `/forge`", text)
        self.assertIn("browser_use", text)
        self.assertIn(TERMINAL_COMMAND, text)
        self.assertIn("~/.hermes/skills/<category>/forge/SKILL.md", text)

    def test_desktop_prompt_forbids_browser(self):
        script = (SITE / "script.js").read_text(encoding="utf-8")
        self.assertIn("TERMINAL_COMMAND", script)
        self.assertIn("DESKTOP_PROMPT", script)
        self.assertIn("browser_use", script)
        self.assertIn("--name forge", script)
        self.assertIn(SKILL_URL, script)

    def test_landing_page_has_two_ctas(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Copy Desktop prompt", html)
        self.assertIn("Copy terminal command", html)
        self.assertIn("copy-desktop", html)
        self.assertIn("copy-terminal", html)
        self.assertNotRegex(html, r"type /forge")

    def test_start_and_index_use_named_install(self):
        start = (SITE / "public" / "start.md").read_text(encoding="utf-8")
        index = json.loads((SITE / "public" / ".well-known" / "skills" / "index.json").read_text(encoding="utf-8"))
        self.assertIn(TERMINAL_COMMAND, start)
        self.assertIn("Do not require `/forge`", start)
        self.assertEqual(index["skills"][0]["name"], "forge")
        self.assertEqual(index["skills"][0]["install"], TERMINAL_COMMAND)
        self.assertLessEqual(len(index["skills"][0]["description"]), 60)

    def test_install_wrapper_writes_skill_directory(self):
        script = (SITE / "public" / "install.sh").read_text(encoding="utf-8")
        self.assertIn("--name forge", script)
        self.assertIn("skills/software-development/forge", script)
        self.assertIn("SKILL.md", script)
        self.assertNotRegex(script, r"type /forge")

    def test_no_goal_alias(self):
        for rel in (
            "site/public/SKILL.md",
            "site/public/start.md",
            "site/public/llms.txt",
            "site/index.html",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"/goal.*alias|alias.*/goal", text, re.I))


if __name__ == "__main__":
    unittest.main()
