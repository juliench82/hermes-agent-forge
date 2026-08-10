from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json

def canonical_manifest(manifest):
    return json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def manifest_hash(manifest):
    return sha256(canonical_manifest(manifest).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class ApprovalRecord:
    manifest_hash: str
    actor: str
    approved_at: str
    action: str
    @classmethod
    def approve(cls, manifest, actor, action="provision-and-start"):
        if not actor.strip():
            raise ValueError("approval actor is required")
        return cls(manifest_hash(manifest), actor, datetime.now(timezone.utc).isoformat(), action)
    def validates(self, manifest, action="provision-and-start"):
        return self.action == action and self.manifest_hash == manifest_hash(manifest)
    def to_dict(self):
        return asdict(self)
