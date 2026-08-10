from __future__ import annotations

from dataclasses import dataclass
from subprocess import CompletedProcess
from typing import Callable
import subprocess

class BuzzSetupRequired(RuntimeError):
    pass

class BuzzSetupError(RuntimeError):
    pass

@dataclass(frozen=True)
class BuzzSetupResult:
    profile: str
    returncode: int
    configured: bool

def _run(argv: list[str]) -> CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, check=False)

class BuzzSetup:
    def __init__(self, runner: Callable[[list[str]], CompletedProcess[str]] = _run, executable: str = "hermes"):
        self.runner = runner
        self.executable = executable

    def configure(self, profile: str, approved: bool) -> BuzzSetupResult:
        if not approved:
            raise BuzzSetupRequired("separate BUZZ setup approval is required")
        result = self.runner([self.executable, "-p", profile, "gateway", "setup"])
        if result.returncode != 0:
            raise BuzzSetupError(result.stderr or "BUZZ gateway setup failed")
        return BuzzSetupResult(profile=profile, returncode=result.returncode, configured=True)
