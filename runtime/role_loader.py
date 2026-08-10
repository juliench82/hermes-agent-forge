"""
role_loader.py — Install role assets/skills into profile homes and verify loading.
"""

from pathlib import Path

def install_role_assets(profile_name: str):
    """Install role assets/skills into the profile's skills directory."""
    home = Path.home() / ".hermes" / "profiles" / profile_name
    skills_dir = home / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skills_dir / f"{profile_name}_role.md"
    if not skill_file.exists():
        skill_file.write_text(f"# {profile_name} role\n\nThis is a placeholder role skill for {profile_name}.\n")
    return skills_dir
