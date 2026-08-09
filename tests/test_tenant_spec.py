import copy
import json
import unittest
from pathlib import Path
from runtime.tenant_spec import TenantSpecValidationError, validate_tenant_spec
ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "invoice-collections.tenant-spec.json"
class TenantSpecTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(EXAMPLE.read_text())
    def test_invoice_collections_example_is_valid(self):
        validate_tenant_spec(self.spec)
    def test_requires_immutable_audit(self):
        spec = copy.deepcopy(self.spec); spec["security"]["audit"]["enabled"] = False
        with self.assertRaisesRegex(TenantSpecValidationError, "audit"): validate_tenant_spec(spec)
    def test_rejects_literal_secret(self):
        spec = copy.deepcopy(self.spec); spec["connectors"][0]["token"] = "do-not-store-secrets-here"
        with self.assertRaisesRegex(TenantSpecValidationError, "literal secrets"): validate_tenant_spec(spec)
    def test_rejects_unknown_connector_scope(self):
        spec = copy.deepcopy(self.spec); spec["agents"][0]["connectors"][0]["scopes"].append("invoices.write")
        with self.assertRaisesRegex(TenantSpecValidationError, "scopes not granted"): validate_tenant_spec(spec)
    def test_irreversible_action_requires_confirmation(self):
        spec = copy.deepcopy(self.spec); spec["agents"][1]["permissions"]["confirmation"]["required"] = False
        with self.assertRaisesRegex(TenantSpecValidationError, "require confirmation"): validate_tenant_spec(spec)
    def test_rejects_delegation_cycle(self):
        spec = copy.deepcopy(self.spec); spec["agents"][0]["delegates"] = {"allow": ["collections-supervisor"]}
        with self.assertRaisesRegex(TenantSpecValidationError, "cycle"): validate_tenant_spec(spec)
if __name__ == "__main__": unittest.main()
