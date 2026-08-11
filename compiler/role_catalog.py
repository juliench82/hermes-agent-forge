"""Use-case-driven role catalog for adaptive team provisioning."""
from __future__ import annotations
from typing import Dict, List, Tuple

# Role descriptions for each profile ID
ROLE_DESCRIPTIONS = {
    # Software/SaaS roles
    "orchestrator": "Coordinate planning, delegation, and consolidation across the team.",
    "product-strategist": "Define product briefs, acceptance criteria, and roadmap priorities.",
    "architect": "Design technical architecture, evaluate trade-offs, and specify interfaces.",
    "builder": "Implement approved features in isolated workspace with tests.",
    "quality-guardian": "Enforce tests, regression checks, security review, and release readiness.",
    "self-improver": "Continuously refine skills, memory, and workflows from observed outcomes.",
    "devops-security": "Manage infrastructure, CI/CD, secrets, and security hardening.",
    # Music/band promotion roles
    "marketing-lead": "Plan and execute marketing campaigns, track performance metrics.",
    "social-media-manager": "Create and schedule posts, engage with fans, monitor trends.",
    "content-creator": "Produce multimedia content (video, audio, graphics) for promotion.",
    "booking-agent": "Manage gig bookings, negotiate contracts, coordinate logistics.",
    "merch-manager": "Design, source, and sell merchandise; manage inventory and fulfillment.",
    # E-commerce support roles
    "support-agent": "Handle customer inquiries, returns, and issue resolution.",
    "order-manager": "Track orders, manage fulfillment, coordinate with logistics.",
}

# Use case catalog: (use_case_id) -> list of (profile_id, description)
# Each use case supports team sizes 3, 5, or 7
USE_CASE_CATALOG: Dict[str, Dict[int, List[str]]] = {
    "solo-founder-saas": {
        3: ["orchestrator", "builder", "quality-guardian"],
        5: ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"],
        7: ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian", "self-improver", "devops-security"],
    },
    "music-band-promotion": {
        3: ["orchestrator", "social-media-manager", "content-creator"],
        5: ["orchestrator", "marketing-lead", "social-media-manager", "content-creator", "booking-agent"],
        7: ["orchestrator", "marketing-lead", "social-media-manager", "content-creator", "booking-agent", "merch-manager", "self-improver"],
    },
    "e-commerce-support": {
        3: ["orchestrator", "support-agent", "order-manager"],
        5: ["orchestrator", "product-strategist", "support-agent", "order-manager", "quality-guardian"],
        7: ["orchestrator", "product-strategist", "architect", "support-agent", "order-manager", "quality-guardian", "devops-security"],
    },
}

USE_CASE_DESCRIPTIONS = {
    "solo-founder-saas": "Solo founder building a SaaS product (MVP, architecture, implementation).",
    "music-band-promotion": "Musician or band promoting releases, gigs, and fan engagement.",
    "e-commerce-support": "E-commerce store handling customer support and order management.",
}


class RoleCatalogError(ValueError):
    """Raised when role catalog lookup fails."""
    pass


def list_use_cases() -> List[str]:
    """Return list of supported use case IDs."""
    return sorted(USE_CASE_CATALOG.keys())


def get_profiles(use_case: str, team_size: int) -> List[str]:
    """
    Return list of profile IDs for the given use case and team size.
    
    Raises RoleCatalogError if use case or team size is unsupported.
    """
    if use_case not in USE_CASE_CATALOG:
        raise RoleCatalogError(f"unsupported use case: {use_case}; supported: {list_use_cases()}")
    if team_size not in (3, 5, 7):
        raise RoleCatalogError(f"unsupported team size: {team_size}; must be 3, 5, or 7")
    
    profiles = USE_CASE_CATALOG[use_case].get(team_size)
    if not profiles:
        raise RoleCatalogError(f"no profile mapping for use_case={use_case}, team_size={team_size}")
    
    if len(profiles) > 7:
        raise RoleCatalogError(f"profile count exceeds maximum of 7: {len(profiles)}")
    
    return profiles


def get_role_description(profile_id: str) -> str:
    """Return the role description for a profile ID."""
    return ROLE_DESCRIPTIONS.get(profile_id, f"Role description for {profile_id} not found.")


def get_use_case_description(use_case: str) -> str:
    """Return the description for a use case ID."""
    return USE_CASE_DESCRIPTIONS.get(use_case, f"Description for {use_case} not found.")


def validate_profiles(profiles: List[str]) -> None:
    """
    Validate that a list of profile IDs is well-formed.
    
    Raises RoleCatalogError if validation fails.
    """
    if not profiles:
        raise RoleCatalogError("profile list cannot be empty")
    if len(profiles) > 7:
        raise RoleCatalogError(f"profile count exceeds maximum of 7: {len(profiles)}")
    for profile_id in profiles:
        if not isinstance(profile_id, str) or not profile_id:
            raise RoleCatalogError(f"invalid profile ID: {profile_id!r}")
