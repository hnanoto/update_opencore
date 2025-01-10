import os
import sys
from logger import log, get_translation, RED, YELLOW, GREEN, NC

def check_environment():
    """Verifica o ambiente e permissões."""
    log(f"{YELLOW}{get_translation('environment_check', fallback_to_key=False)}{NC}")
    if not sys.platform.startswith("darwin"):
        log(f"{RED}{get_translation('environment_error_macos', fallback_to_key=False)}{NC}")
        sys.exit(1)
    if os.geteuid() != 0:
        log(f"{YELLOW}{get_translation('environment_error_root', fallback_to_key=False)}{NC}")
        os.execvp("sudo", ["sudo"] + sys.argv)
    log(f"{GREEN}{get_translation('environment_success', fallback_to_key=False)}{NC}")