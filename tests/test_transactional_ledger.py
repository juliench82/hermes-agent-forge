import tempfile
from pathlib import Path
import unittest

from runtime.transactional_ledger import (
    InstallationLedger,
    InstallationState,
    LedgerError,
    OperationResult,
)


class RecordingNotifier:
    def __init__(self):
        self.ledgers = []

    def notify(self, ledger):
        self.ledgers.append(ledger)


class TransactionalLedgerTests(unittest.TestCase):
    def setUp(self):
        self.plan = {"profiles": ["builder"], "skills": {"builder": ["testing"]}}

    def approved_ledger(self):
        ledger = InstallationLedger(self.plan, max_repair_attempts=1)
        ledger.approve(ledger.plan_hash)
        return ledger

    def test_approval_is_bound_to_exact_plan(self):
        ledger = InstallationLedger(self.plan)
        with self.assertRaises(LedgerError):
            ledger.approve("not-the-plan-hash")
        self.assertEqual(ledger.state, InstallationState.PLANNED)
        ledger.approve(ledger.plan_hash)
        self.assertEqual(ledger.state, InstallationState.APPROVED)

    def test_completion_requires_verified_required_operations(self):
        ledger = self.approved_ledger()
        ledger.begin_provisioning()
        ledger.record(OperationResult("profile", "builder", True, "created", "command succeeded"))
        ledger.begin_verification()
        with self.assertRaises(LedgerError):
            ledger.complete()
        ledger.mark_partial()
        ledger.begin_repair()
        ledger.record(OperationResult("profile", "builder", True, "verified", "profile listed"))
        ledger.finish_repair()
        ledger.complete()
        self.assertEqual(ledger.state, InstallationState.COMPLETED)
        self.assertEqual(len(ledger.operations), 1)

    def test_invalid_operation_kind_and_transition_are_rejected(self):
        ledger = self.approved_ledger()
        with self.assertRaises(LedgerError):
            ledger.record(OperationResult("connector", "buzz", True, "verified", "listing"))
        ledger.begin_provisioning()
        with self.assertRaises(LedgerError):
            ledger.finish_repair()

    def test_repair_exhaustion_escalates_to_administrator(self):
        ledger = self.approved_ledger()
        ledger.begin_provisioning()
        ledger.begin_verification()
        ledger.mark_partial()
        ledger.begin_repair()
        ledger.finish_repair()
        notifier = RecordingNotifier()
        ledger.begin_repair(notifier)
        self.assertEqual(ledger.state, InstallationState.ADMIN_ACTION_REQUIRED)
        self.assertEqual(notifier.ledgers, [ledger])

    def test_persist_and_load_preserves_resume_state(self):
        ledger = self.approved_ledger()
        ledger.begin_provisioning()
        ledger.record(OperationResult("skill", "pytest-runner", True, "verified", "installed listing"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            ledger.persist(path)
            loaded = InstallationLedger.load(path)
        self.assertEqual(loaded.plan_hash, ledger.plan_hash)
        self.assertEqual(loaded.state, InstallationState.PROVISIONING)
        self.assertEqual(loaded.operations, ledger.operations)


if __name__ == "__main__":
    unittest.main()
