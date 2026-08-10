from __future__ import annotations

from dataclasses import dataclass
from subprocess import CompletedProcess
from typing import Callable, Sequence
import subprocess

from runtime.capabilities import Capability, REQUIRED_CAPABILITIES

Runner = Callable[[list[str]], CompletedProcess[str]]


@dataclass(frozen=True)
class ProbeResult:
    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


def _run(argv: list[str]) -> CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, check=False)


class HermesCliProbe:
    """HermesRuntimeProbe implementation that only touches documented CLI help/version surfaces."""

    def __init__(self, executable: str = "hermes", runner: Runner = _run):
        self.executable = executable
        self.runner = runner

    def _probe(self, argv: list[str]) -> ProbeResult:
        try:
            result = self.runner([self.executable, *argv])
        except FileNotFoundError:
            return ProbeResult(tuple(argv), 127, "", "Hermes executable was not found on PATH")
        return ProbeResult(tuple(argv), result.returncode, result.stdout, result.stderr)

    def runtime_identity(self) -> tuple[str, str | None]:
        version = self._probe(["--version"])
        return "Hermes", version.stdout.strip() or None

    def capabilities(self) -> Sequence[Capability]:
        checks: dict[str, list[str] | None] = {
            "profile.create": ["profile", "create", "--help"],
            "profile.status": ["profile", "list", "--help"],
            "profile.start": ["--help"],
            "runtime.configure": ["gateway", "setup", "--help"],
            "runtime.isolation": ["profile", "create", "--help"],
            "runtime.audit": None,
            "runtime.confirmation": None,
            "runtime.secrets": None,
        }

        capabilities: list[Capability] = []
        for name in sorted(REQUIRED_CAPABILITIES):
            argv = checks.get(name)
            if argv is None:
                capabilities.append(
                    Capability(
                        name=name,
                        available=False,
                        remediation="This capability is enforced inside Hermes Agent Forge; Hermes CLI does not expose a direct proof surface.",
                    )
                )
                continue

            result = self._probe(argv)
            surface = " ".join((self.executable, *argv))
            available = result.returncode == 0
            remediation: str | None = None
            if not available:
                stderr = (result.stderr or "").strip()
                if result.returncode == 127 or "not found" in stderr.lower():
                    remediation = f"{surface} is not supported by the installed Hermes version."
                else:
                    remediation = stderr or f"{surface} did not succeed."
            capabilities.append(
                Capability(
                    name=name,
                    available=available,
                    surface=surface if available else None,
                    remediation=remediation,
                )
            )
        return tuple(capabilities)
