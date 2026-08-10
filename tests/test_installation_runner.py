from pathlib import Path

from runtime.approval import ApprovalRecord
from runtime.buzz_setup import BuzzSetup
from runtime.installation_runner import AggregateInstaller
from runtime.installation_store import InstallationLedger
from runtime.role_assets import RoleAssetInstaller

class Provisioned:
    profiles = ("orchestrator", "product-strategist", "architect", "builder", "quality-guardian")
    primary = "orchestrator"

class Provisioner:
    def provision(self, ledger, state, manifest): return Provisioned()

def make(tmp_path, smoke, start=lambda: True, running=lambda: True):
    source = tmp_path / "role"; profile = tmp_path / "profile"; source.mkdir(); profile.mkdir()
    (source / "skill.md").write_text("role", encoding="utf-8")
    manifest = {"obsidian": {"choice": "SKIP"}, "buzz": {"enabled": False}, "role_assets": {role: {"source_root": str(source), "profile_root": str(profile / role), "mapping": {"skill.md": "skill.md"}} for role in Provisioned.profiles}}
    ledger = InstallationLedger(tmp_path / "state.json"); state = ledger.initialize({"repository": "forge"}); ledger.record_approval(state, ApprovalRecord.approve(manifest, "human"))
    return AggregateInstaller(ledger, Provisioner(), BuzzSetup(), RoleAssetInstaller(), smoke, start, running), state, manifest

def test_failed_smoke_never_reaches_running(tmp_path):
    installer, state, manifest = make(tmp_path, lambda _: {"passed": False})
    result = installer.run(state, manifest)
    assert result.status == "failed"
    assert installer.ledger.load()["events"][-1]["event"] == "failed"

def test_success_requires_observed_running_status(tmp_path):
    installer, state, manifest = make(tmp_path, lambda _: {"passed": True}, running=lambda: False)
    result = installer.run(state, manifest)
    assert result.status == "failed"

def test_success_records_running_only_after_start_and_smoke(tmp_path):
    installer, state, manifest = make(tmp_path, lambda _: {"passed": True})
    result = installer.run(state, manifest)
    assert result.status == "running"
    assert installer.ledger.load()["events"][-1]["event"] == "running"
