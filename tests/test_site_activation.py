from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).parents[1]
SITE = ROOT / "site"
SKILL_URL = "https://hermes-agents-forge.vercel.app/SKILL.md"
LOCAL_PATH = "~/.hermes/skills/software-development/forge/SKILL.md"
TERMINAL_COMMAND = (
    "mkdir -p ~/.hermes/skills/software-development/forge && "
    f"curl -fsSL {SKILL_URL} -o {LOCAL_PATH}"
)
QUESTION = "What do you want Hermes to accomplish for you?"


def desktop_prompt_from_script(script: str) -> str:
    match = re.search(r"const DESKTOP_PROMPT = \[(.*?)\]\.join", script, re.S)
    if not match:
        return ""
    parts = re.findall(r'"((?:\\.|[^"\\])*)"', match.group(1))
    return "\n".join(part.encode("utf-8").decode("unicode_escape") for part in parts)


class SiteActivationTests(unittest.TestCase):
    def test_canonical_skill_files_match(self):
        public = (SITE / "public" / "SKILL.md").read_text(encoding="utf-8")
        tap = (ROOT / "skills" / "forge" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(public, tap)

    def test_skill_avoids_scanner_triggers_and_hub_install(self):
        text = (SITE / "public" / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name: forge$")
        self.assertIn(QUESTION, text)
        self.assertIn("Never treat `/goal` as an alias", text)
        self.assertIn("Do not require `/forge`", text)
        self.assertIn("skip environment probes", text)
        self.assertNotIn("sudo", text.lower())
        self.assertNotIn("privileged", text.lower())
        self.assertIn("Do not use `hermes skills install`", text)

    def test_desktop_prompt_uses_local_curl(self):
        script = (SITE / "script.js").read_text(encoding="utf-8")
        prompt = desktop_prompt_from_script(script)
        self.assertTrue(prompt)
        self.assertNotIn(SKILL_URL, prompt)
        self.assertNotIn("`https://", prompt)
        self.assertIn("Do not run hermes skills install", prompt)
        self.assertIn("curl -fsSL", prompt)
        self.assertIn("software-development/forge", prompt)
        self.assertIn("printf", prompt)
        self.assertIn("@url:", prompt)
        self.assertIn("immediately ask", prompt)
        self.assertIn(TERMINAL_COMMAND, script)

    def test_landing_page_has_two_ctas(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Copy Desktop prompt", html)
        self.assertIn("Copy terminal command", html)
        self.assertNotRegex(html, r"type /forge")

    def test_start_and_index_use_local_install(self):
        start = (SITE / "public" / "start.md").read_text(encoding="utf-8")
        index = json.loads((SITE / "public" / ".well-known" / "skills" / "index.json").read_text(encoding="utf-8"))
        self.assertIn("curl -fsSL", start)
        self.assertIn("Do not use `hermes skills install`", start)
        self.assertEqual(index["skills"][0]["name"], "forge")
        self.assertEqual(index["skills"][0]["install"], TERMINAL_COMMAND)
        self.assertLessEqual(len(index["skills"][0]["description"]), 60)

    def test_install_wrapper_writes_skill_directory(self):
        script = (SITE / "public" / "install.sh").read_text(encoding="utf-8")
        self.assertIn("skills/software-development/forge", script)
        self.assertIn("curl -fsSL", script)
        self.assertNotIn("hermes skills install", script)

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
