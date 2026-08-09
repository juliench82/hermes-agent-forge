"""Secret access control: per-agent secret references, no values in prompts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SecretRef:
    name: str
    ref: str  # e.g., vault:secret/github/token
    agent_ids: List[str]


class SecretsPolicy:
    def __init__(self, secrets: List[SecretRef]) -> None:
        self.secrets = secrets
        self._by_ref = {s.ref: s for s in secrets}

    def can_access(self, agent_id: str, ref: str) -> bool:
        secret = self._by_ref.get(ref)
        if not secret:
            return False
        return agent_id in secret.agent_ids

    def for_agent(self, agent_id: str) -> List[SecretRef]:
        return [s for s in self.secrets if agent_id in s.agent_ids]


def build_secrets_policy(policy_rows: List[Dict[str, Any]]) -> SecretsPolicy:
    """Build SecretsPolicy from manifest secrets_policy rows."""
    secrets: List[SecretRef] = []
    for row in policy_rows:
        secrets.append(
            SecretRef(
                name=row.get("name", row["secret_ref"].split("/")[-1]),
                ref=row["secret_ref"],
                agent_ids=[row["agent"]],
            )
        )
    return SecretsPolicy(secrets)
