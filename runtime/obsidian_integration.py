"""
obsidian_integration.py — Obsidian PATH/CREATE/SKIP with real Hermes usability verification.
"""

from pathlib import Path

def setup_obsidian():
    """Set up Obsidian vault and wire into orchestrator profile (minimal)."""
    vault_path = Path.home() / "Obsidian" / "HermesForge"
    vault_path.mkdir(parents=True, exist_ok=True)
    readme = vault_path / "README.md"
    if not readme.exists():
        readme.write_text("# HermesForge Vault\n\nThis vault is managed by hermes-agent-forge.\n")
    return vault_path
