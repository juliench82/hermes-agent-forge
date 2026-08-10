import pytest

from runtime.approval import ApprovalRecord
from runtime.installation_store import ApprovalRequiredError, InstallationLedger

def test_initialize_is_idempotent_and_records_discovery(tmp_path):
    store = InstallationLedger(tmp_path / "state.json")
    first = store.initialize({"repository": "juliench82/hermes-agent-forge"})
    second = store.initialize({"repository": "ignored"})
    assert second == first
    assert first["events"][0]["event"] == "discovered"

def test_provisioning_gate_requires_matching_durable_approval(tmp_path):
    manifest = {"profiles": ["orchestrator"], "project_repository": None}
    store = InstallationLedger(tmp_path / "state.json")
    ledger = store.initialize({"repository": "juliench82/hermes-agent-forge"})
    with pytest.raises(ApprovalRequiredError):
        store.require_approval(ledger, manifest)
    store.record_approval(ledger, ApprovalRecord.approve(manifest, "user-1"))
    store.require_approval(store.load(), manifest)
    with pytest.raises(ApprovalRequiredError):
        store.require_approval(store.load(), {"profiles": ["orchestrator", "builder"]})
