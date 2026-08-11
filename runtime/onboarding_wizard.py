"""
onboarding_wizard.py — Adaptive onboarding wizard for provider/model/config.
"""

import subprocess
import json

def run_onboarding_wizard():
    """Collect provider/model/config choices from the user."""
    print("\n=== Hermes Forge Onboarding ===")
    print("\nThis installer will provision a 5-profile control room.")
    print("\nFirst, enable YOLO mode in Hermes: run /yolo in your Hermes session.\n")
    
    # Provider selection
    print("Select your model provider:")
    print("1. Nous Portal (OAuth — recommended)")
    print("2. API-key provider (Nvidia, OpenAI, etc.)")
    print("3. Custom OpenAI-compatible endpoint")
    print("4. Skip provider setup (configure manually later)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    provider_config = {"choice": choice}
    
    if choice == "1":
        print("\nRunning: hermes setup --portal")
        result = subprocess.run(["hermes", "setup", "--portal"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print(f"Warning: Portal setup failed: {result.stderr}")
        provider_config["provider"] = "nous"
        provider_config["setup_method"] = "oauth"
    elif choice == "2":
        print("\nRunning: hermes model (interactive)")
        result = subprocess.run(["hermes", "model"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print(f"Warning: Model setup failed: {result.stderr}")
        provider_config["provider"] = "api_key"
        provider_config["setup_method"] = "interactive"
    elif choice == "3":
        endpoint = input("Enter custom endpoint URL: ").strip()
        model = input("Enter model ID: ").strip()
        key_env = input("Enter environment variable name for API key: ").strip()
        provider_config["provider"] = "custom"
        provider_config["endpoint"] = endpoint
        provider_config["model"] = model
        provider_config["key_env"] = key_env
    else:
        provider_config["provider"] = "skip"
    
    # Model policy
    print("\nModel policy:")
    print("1. One shared model for all profiles (default)")
    print("2. Override per role (advanced)")
    model_choice = input("Enter choice (1-2): ").strip()
    provider_config["model_policy"] = "shared" if model_choice == "1" else "per_role"
    
    # Operational preferences
    print("\nOperational preferences:")
    obsidian_choice = input("Obsidian vault: create Forge vault / skip? (create/skip): ").strip()
    buzz_choice = input("BUZZ: configure now / skip? (configure/skip): ").strip()
    gateway_choice = input("Gateway: start after smoke tests / provision only? (start/provision): ").strip()
    
    provider_config["obsidian"] = obsidian_choice
    provider_config["buzz"] = buzz_choice
    provider_config["gateway"] = gateway_choice
    
    return provider_config
