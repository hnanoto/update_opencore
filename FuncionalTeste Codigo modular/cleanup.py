import os
import shutil
from logger import log, YELLOW, GREEN, NC

def cleanup():
    """Limpa arquivos temporários."""
    log(f"{YELLOW}Limpando arquivos temporários...{NC}")
    try:
        os.remove("OpenCore.zip")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree("OpenCore")
    except FileNotFoundError:
        pass
    try:
        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_new_keys.py"))
    except FileNotFoundError:
        pass
    log(f"{GREEN}Limpeza concluída.{NC}")