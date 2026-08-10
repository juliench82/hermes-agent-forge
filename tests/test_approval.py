import pytest
from runtime.approval import ApprovalRecord, manifest_hash

def test_approval_is_bound_to_the_exact_manifest_and_action():
    manifest = {"profiles": ["orchestrator"], "project_repository": None}
    record = ApprovalRecord.approve(manifest, "user-1")
    assert record.validates(manifest)
    assert record.manifest_hash == manifest_hash(manifest)
    assert not record.validates(manifest, "provision-only")

def test_material_manifest_change_invalidates_approval():
    manifest = {"profiles": ["orchestrator"]}
    record = ApprovalRecord.approve(manifest, "user-1")
    assert not record.validates({"profiles": ["orchestrator", "builder"]})

def test_approval_requires_an_identified_human_actor():
    with pytest.raises(ValueError):
        ApprovalRecord.approve({}, " ")
