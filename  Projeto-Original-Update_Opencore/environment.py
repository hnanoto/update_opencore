import os
import sys
from logger import log, RED, YELLOW, GREEN, NC

def check_environment():
    """Verifica o ambiente e permissões."""
    log(f"{YELLOW}Verificando ambiente...{NC}")
    if not sys.platform.startswith("darwin"):
        log(f"{RED}Erro: Este script deve ser executado no macOS.{NC}")
        sys.exit(1)
    if os.geteuid() != 0:
        log(f"{YELLOW}Este script requer permissões de administrador. Solicitando sudo...{NC}")
        os.execvp("sudo", ["sudo"] + sys.argv)
    log(f"{GREEN}Ambiente verificado com sucesso.{NC}")