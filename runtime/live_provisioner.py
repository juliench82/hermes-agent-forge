from dataclasses import dataclass
from pathlib import Path
from subprocess import CompletedProcess
from typing import Callable
import subprocess

from runtime.installation_store import InstallationLedger

PROFILES = ("orchestrator", "product-strategist", "architect", "builder", "quality-guardian")

class ProvisioningError(RuntimeError): pass

@dataclass(frozen=True)
class ProvisionResult:
    profiles: tuple[str, ...]
    primary: str

def _run(argv): return subprocess.run(argv, text=True, capture_output=True, check=False)

class HermesProvisioner:
    def __init__(self, home: Path, runner: Callable = _run, executable="hermes"):
        self.home, self.runner, self.executable = home, runner, executable
    def command(self, *args):
        result = self.runner([self.executable, *args])
        if result.returncode: raise ProvisioningError(result.stderr or "Hermes command failed")
        return result.stdout
    def provision(self, ledger: InstallationLedger, state, manifest):
        if manifest.get("project_repository"):
            raise ProvisioningError("user project repository connections are disabled by default")
        ledger.require_approval(state, manifest)
        listed = self.command("profile", "list")
        for name in PROFILES:
            if name not in listed: self.command("profile", "create", name)
            marker = self.home / "profiles" / name / "SOUL.md"
            if not marker.is_file(): raise ProvisioningError(f"profile marker missing: {marker}")
        self.command("profile", "use", "orchestrator")
        ledger.append(state, "profiles-provisioned", {"profiles": list(PROFILES), "primary": "orchestrator"})
        return ProvisionResult(PROFILES, "orchestrator")
