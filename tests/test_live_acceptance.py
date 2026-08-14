import unittest
from pathlib import Path

from runtime.live_acceptance import LiveAcceptanceConfig, LiveAcceptanceError


class LiveAcceptanceConfigTests(unittest.TestCase):
    def test_live_tests_are_disabled_by_default(self):
        config = LiveAcceptanceConfig.from_environment({})
        self.assertFalse(config.enabled)
        with self.assertRaises(LiveAcceptanceError):
            config.require_enabled()

    def test_enabled_tests_require_absolute_isolated_home(self):
        with self.assertRaises(LiveAcceptanceError):
            LiveAcceptanceConfig.from_environment({"HERMES_LIVE_TESTS": "1"})
        with self.assertRaises(LiveAcceptanceError):
            LiveAcceptanceConfig.from_environment(
                {"HERMES_LIVE_TESTS": "1", "HERMES_LIVE_HOME": "relative"}
            )

    def test_enabled_config_builds_list_argument_command(self):
        config = LiveAcceptanceConfig.from_environment(
            {"HERMES_LIVE_TESTS": "1", "HERMES_LIVE_HOME": "/tmp/hermes-live"}
        )
        self.assertEqual(config.command("--version"), ("hermes", "--version"))
        self.assertEqual(config.hermes_home, Path("/tmp/hermes-live"))

    def test_timeout_is_bounded(self):
        for value in ("0", "301", "not-a-number"):
            with self.subTest(value=value):
                with self.assertRaises(LiveAcceptanceError):
                    LiveAcceptanceConfig.from_environment(
                        {
                            "HERMES_LIVE_TESTS": "1",
                            "HERMES_LIVE_HOME": "/tmp/hermes-live",
                            "HERMES_LIVE_TIMEOUT": value,
                        }
                    )

    def test_command_rejects_empty_arguments(self):
        config = LiveAcceptanceConfig.from_environment(
            {"HERMES_LIVE_TESTS": "1", "HERMES_LIVE_HOME": "/tmp/hermes-live"}
        )
        with self.assertRaises(LiveAcceptanceError):
            config.command("--version", "")


if __name__ == "__main__":
    unittest.main()
