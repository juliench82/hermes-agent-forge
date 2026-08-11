import subprocess
import unittest

from runtime.native_runtime import activate_yolo, run_terminal, terminal_command


class NativeRuntimeTests(unittest.TestCase):
    def test_yolo_success_is_verified_from_return_code(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, stdout="enabled", stderr="")
        result = activate_yolo(runner=runner)
        self.assertTrue(result.ok)
        self.assertEqual(result.command, ("hermes", "chat", "--command", "/yolo"))

    def test_yolo_failure_is_not_suppressed(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 2, stdout="", stderr="denied")
        result = activate_yolo(runner=runner)
        self.assertFalse(result.ok)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "denied")

    def test_terminal_command_is_explicit(self):
        self.assertEqual(terminal_command(["./install.sh"]), ("hermes", "terminal", "exec", "--", "./install.sh"))

    def test_terminal_result_is_propagated(self):
        def runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")
        result = run_terminal(["./install.sh"], runner=runner)
        self.assertTrue(result.ok)
        self.assertEqual(result.stdout, "ok")


if __name__ == "__main__":
    unittest.main()
