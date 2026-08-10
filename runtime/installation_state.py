from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json

class InstallationStatus(str, Enum):
    DISCOVERED="discovered"; ONBOARDING="onboarding"; PROPOSED="proposed"; APPROVED="approved"; PROVISIONING="provisioning"; PROVISIONED="provisioned"; SMOKE_TESTED="smoke-tested"; RUNNING="running"; BLOCKED="blocked"; FAILED="failed"; STOPPED="stopped"

_ALLOWED = {
 InstallationStatus.DISCOVERED:{InstallationStatus.ONBOARDING,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.ONBOARDING:{InstallationStatus.PROPOSED,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.PROPOSED:{InstallationStatus.APPROVED,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.APPROVED:{InstallationStatus.PROVISIONING,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.PROVISIONING:{InstallationStatus.PROVISIONED,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.PROVISIONED:{InstallationStatus.SMOKE_TESTED,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.SMOKE_TESTED:{InstallationStatus.RUNNING,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.RUNNING:{InstallationStatus.STOPPED,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.STOPPED:{InstallationStatus.PROVISIONING,InstallationStatus.BLOCKED,InstallationStatus.FAILED},
 InstallationStatus.BLOCKED:set(), InstallationStatus.FAILED:set()}

class StateTransitionError(ValueError): pass
def now(): return datetime.now(timezone.utc).isoformat()

@dataclass
class InstallationState:
    installation_id: str
    bootstrap: dict
    status: InstallationStatus = InstallationStatus.DISCOVERED
    events: list = field(default_factory=list)
    provisioning: dict = field(default_factory=dict)
    smoke_tests: dict = field(default_factory=dict)
    @classmethod
    def discovered(cls, bootstrap):
        installation_id=sha256(json.dumps(bootstrap,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        state=cls(installation_id,dict(bootstrap)); state.events.append({"at":now(),"from":None,"to":state.status.value}); return state
    def transition(self, target):
        if target == self.status: return
        if target not in _ALLOWED[self.status]: raise StateTransitionError(f"invalid transition: {self.status.value} -> {target.value}")
        if target is InstallationStatus.RUNNING and not (self.provisioning.get("complete") and self.smoke_tests.get("passed")):
            raise StateTransitionError("running requires complete provisioning and passing smoke tests")
        prior=self.status; self.status=target; self.events.append({"at":now(),"from":prior.value,"to":target.value})
    def to_dict(self):
        data=asdict(self); data["status"]=self.status.value; return data
