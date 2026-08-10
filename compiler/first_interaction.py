"""Sprint 8: deterministic first orchestrator interaction for solo founders."""
from __future__ import annotations
from typing import Any

REQUIRED_REQUEST = "Help me define the smallest valuable MVP slice. Do not connect a user project repository yet."

class FirstInteractionError(ValueError):
    pass

def produce_first_interaction(activation_summary: dict[str, Any], request: str) -> dict[str, Any]:
    if activation_summary.get("team") != "solo-founder-saas":
        raise FirstInteractionError("first interaction requires solo-founder-saas activation")
    if activation_summary.get("userProjectRepository", {}).get("connected") is not False:
        raise FirstInteractionError("user project repository must remain disconnected")
    if request != REQUIRED_REQUEST:
        raise FirstInteractionError("unsupported Sprint 8 first interaction request")
    return {
        "productBrief": "Define a smallest valuable SaaS MVP slice that validates one founder-chosen customer problem before broader implementation.",
        "assumptions": [
            "The founder has a target problem worth validating.",
            "The first slice should minimise scope, dependencies, and irreversible actions.",
            "No existing application repository is needed for product discovery.",
        ],
        "targetUser": "The primary user who experiences the selected problem frequently enough to evaluate the MVP.",
        "acceptanceCriteria": [
            "The problem, target user, and promised outcome are stated in plain language.",
            "The MVP contains one end-to-end user journey and excludes non-essential features.",
            "Success can be evaluated with a measurable user or business signal.",
            "No user project repository, connector, deployment, or external write is required for this stage.",
        ],
        "recommendedNextStep": "Ask the product-strategist to turn the selected problem into a concise product brief and acceptance criteria; then request an architecture proposal before deciding whether a user project repository is needed.",
        "userProjectRepository": {"connected": False},
        "sideEffects": {"implementationStarted": False, "connectorsConnected": False, "externalWrites": False},
    }
