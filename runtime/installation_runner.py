from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from runtime.buzz_setup import BuzzSetup
from runtime.live_provisioner import HermesProvisioner
from runtime.obsidian_setup import resolve_vault
from runtime.role_assets import RoleAssetInstaller
from runtime.installation_store import InstallationLedger

@dataclass(frozen=True)
class InstallationResult:
    status: str
    details: Mapping[str, Any]

class AggregateInstaller:
    def __init__(self, ledger: InstallationLedger, provisioner: HermesProvisioner, buzz: BuzzSetup, assets: RoleAssetInstaller, smoke_tests: Callable[[Mapping[str, Any]], Mapping[str, Any]], start: Callable[[], bool], running: Callable[[], bool]):
        self.ledger, self.provisioner, self.buzz, self.assets = ledger, provisioner, buzz, assets
        self.smoke_tests, self.start, self.running = smoke_tests, start, running

    def run(self, state: dict[str, Any], manifest: Mapping[str, Any]) -> InstallationResult:
        self.ledger.require_approval(state, manifest)
        self.ledger.append(state, "provisioning-started", {})
        try:
            provisioned = self.provisioner.provision(self.ledger, state, manifest)
            asset_results: dict[str, Any] = {}
            for role in provisioned.profiles:
                spec = manifest.get("role_assets", {}).get(role, {})
                if not spec:
                    raise RuntimeError(f"missing approved role-asset mapping for {role}")
                asset_results[role] = [asset.__dict__ for asset in self.assets.install(Path(spec["source_root"]), Path(spec["profile_root"]), spec["mapping"])]
            obsidian = resolve_vault(manifest.get("obsidian", {}).get("choice", "SKIP"), manifest.get("obsidian", {}).get("path"))
            self.ledger.append(state, "integrations-configured", {"obsidian": obsidian, "assets": asset_results})
            buzz_results = []
            if manifest.get("buzz", {}).get("enabled"):
                if not manifest.get("buzz", {}).get("approved"):
                    raise RuntimeError("separate BUZZ setup approval is required")
                for role in provisioned.profiles:
                    result = self.buzz.configure(role, True)
                    buzz_results.append({"profile": result.profile, "configured": result.configured})
            smoke = dict(self.smoke_tests({"profiles": provisioned.profiles, "obsidian": obsidian, "buzz": buzz_results}))
            self.ledger.append(state, "smoke-tested", smoke)
            if not smoke.get("passed"):
                self.ledger.append(state, "failed", {"reason": "smoke tests failed", "smoke": smoke})
                return InstallationResult("failed", smoke)
            if not self.start() or not self.running():
                self.ledger.append(state, "failed", {"reason": "orchestrator did not reach running status"})
                return InstallationResult("failed", {"smoke": smoke})
            self.ledger.append(state, "running", {"primary": provisioned.primary})
            return InstallationResult("running", {"primary": provisioned.primary, "smoke": smoke})
        except Exception as error:
            self.ledger.append(state, "blocked", {"reason": str(error)})
            return InstallationResult("blocked", {"reason": str(error)})
