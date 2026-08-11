"""Tests for dynamic onboarding prompt generation and response parsing."""
import unittest

from compiler.onboarding_prompt import generate_profile_discovery_prompt, parse_hermes_response, validate_team_structure


class PromptGenerationTests(unittest.TestCase):
    def test_prompt_includes_context_and_json_contract(self):
        prompt = generate_profile_discovery_prompt("Promote my music album", "Musician", ["Release album", "Book gigs"])
        for value in ("Promote my music album", "Musician", "Release album", "JSON", "team_size", "profiles"):
            self.assertIn(value, prompt)

    def test_prompt_includes_preferred_size(self):
        self.assertIn("exactly 7 profiles", generate_profile_discovery_prompt("Test", "Role", ["Goal"], 7))


class ResponseParserTests(unittest.TestCase):
    def test_parse_clean_json(self):
        result = parse_hermes_response('{"team_size": 3, "profiles": [{"name": "lead", "description": "Coordinate the team.", "skills": ["planning"]}, {"name": "builder", "description": "Build the work.", "skills": ["delivery"]}, {"name": "reviewer", "description": "Review results.", "skills": ["quality"]}]}')
        self.assertEqual(result["team_size"], 3)
        self.assertEqual(result["validation_errors"], [])

    def test_parse_json_in_markdown_block(self):
        response = 'Here is the team:\n```json\n{"team_size": 3, "profiles": [{"name": "lead", "description": "Coordinate.", "skills": ["planning"]}, {"name": "builder", "description": "Build.", "skills": ["delivery"]}, {"name": "reviewer", "description": "Review.", "skills": ["quality"]}]}\n```'
        self.assertEqual(parse_hermes_response(response)["team_size"], 3)

    def test_invalid_json_raises(self):
        with self.assertRaises(ValueError):
            parse_hermes_response("not JSON")

    def test_semantic_errors_are_returned(self):
        self.assertTrue(parse_hermes_response('{"team_size": 4, "profiles": []}')["validation_errors"])


class ValidationTests(unittest.TestCase):
    def test_valid_team_passes(self):
        team = {"team_size": 5, "profiles": [{"name": f"profile-{i}", "description": "Desc", "skills": ["skill"]} for i in range(5)]}
        self.assertEqual(validate_team_structure(team), [])

    def test_too_many_profiles_fails(self):
        team = {"team_size": 7, "profiles": [{"name": f"p{i}", "description": "Desc", "skills": ["s"]} for i in range(10)]}
        self.assertTrue(any("7" in error for error in validate_team_structure(team)))

    def test_duplicate_and_unsafe_names_fail(self):
        team = {"team_size": 3, "profiles": [{"name": "Lead", "description": "A", "skills": ["a"]}, {"name": "lead", "description": "B", "skills": ["b"]}, {"name": "bad name", "description": "C", "skills": ["c"]}]}
        errors = validate_team_structure(team)
        self.assertTrue(any("unique" in error for error in errors))
        self.assertTrue(any("safe" in error for error in errors))

    def test_missing_description_and_skills_fail(self):
        team = {"team_size": 3, "profiles": [{"name": "a", "description": "", "skills": []}, {"name": "b", "description": "ok", "skills": ["x"]}, {"name": "c", "description": "ok", "skills": ["x"]}]}
        errors = validate_team_structure(team)
        self.assertTrue(any("description" in error for error in errors))
        self.assertTrue(any("skills" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
