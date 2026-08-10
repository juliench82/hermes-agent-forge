from pathlib import Path

class ObsidianSetupError(RuntimeError): pass

def resolve_vault(choice, value=None):
    if choice == "SKIP": return {"status": "skipped", "path": None}
    path = Path(value).expanduser() if choice == "PATH" and value else Path(value or "Hermes Agent Forge").expanduser()
    if choice == "CREATE": path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir(): raise ObsidianSetupError("Obsidian vault path does not exist")
    probe = path / ".hermes-agent-forge-write-check"
    probe.write_text("ok", encoding="utf-8"); probe.unlink()
    return {"status": "ready", "path": str(path)}
