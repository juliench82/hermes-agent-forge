from subprocess import run

class BuzzSetupRequired(RuntimeError): pass

def run_buzz_setup(profile, approved):
    if not approved: raise BuzzSetupRequired("separate BUZZ setup approval is required")
    # Interactive wizard owns relay/community input and private-key handling.
    return run(["hermes", "-p", profile, "gateway", "setup"], check=False).returncode
