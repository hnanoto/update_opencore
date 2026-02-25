import shutil
import sys
from logger import log, get_translation, RED, YELLOW, GREEN, NC

def check_dependencies():
    """Verifica as dependências."""
    log(f"{YELLOW}{get_translation('dependencies_check', fallback_to_key=True)}{NC}")
    dependencies = ["curl", "unzip", "python3"]
    for cmd in dependencies:
        if not shutil.which(cmd):
            log(f"{RED}{get_translation('dependency_not_found', fallback_to_key=True).format(cmd=cmd)}{NC}")
            if cmd == "python3":
                log(f"{YELLOW}{get_translation('python3_needed', fallback_to_key=True)}{NC}")
            sys.exit(1)
    log(f"{GREEN}{get_translation('dependencies_success', fallback_to_key=True)}{NC}")