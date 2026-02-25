import os
import shutil
from logger import log, get_translation, RED, YELLOW, GREEN, NC

def cleanup():
    """Remove o diretório baixado e o arquivo ZIP original."""
    log(f"{YELLOW}{get_translation('cleaning_temp_files', fallback_to_key=True)}{NC}")
    if os.path.exists("OpenCore"):
        try:
            shutil.rmtree("OpenCore")
        except Exception as e:
            log(f"{RED}Erro ao remover o diretório 'OpenCore': {e}{NC}")
    if os.path.exists("OpenCore.zip"):
        try:
            os.remove("OpenCore.zip")
        except Exception as e:
            log(f"{RED}Erro ao remover 'OpenCore.zip': {e}{NC}")
    log(f"{GREEN}{get_translation('cleaning_done', fallback_to_key=True)}{NC}")