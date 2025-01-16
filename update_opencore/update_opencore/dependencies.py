import shutil
from logger import log, RED, YELLOW, GREEN, NC

def check_dependencies():
    """Verifica as dependências."""
    log(f"{YELLOW}Verificando dependências...{NC}")
    dependencies = ["curl", "unzip", "python3"]
    for cmd in dependencies:
        if not shutil.which(cmd):
            log(f"{RED}Erro: Dependência '{cmd}' não encontrada.{NC}")
            if cmd == "python3":
                log(f"{YELLOW}O Python 3 é necessário para o script. Instale-o através do Homebrew com 'brew install python3'.{NC}")
            sys.exit(1)
    log(f"{GREEN}Todas as dependências estão disponíveis.{NC}")