import os
import shutil
from datetime import datetime
from logger import log, RED, YELLOW, GREEN, NC
import sys

def backup_efi(efi_dir):
    """Cria backup da EFI."""
    efi_backup_dir = os.path.join(efi_dir, f"EFI-Backup-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    log(f"{YELLOW}Criando backup em {efi_backup_dir}...{NC}")
    try:
        # Usando o caminho completo da EFI
        shutil.copytree(os.path.join(efi_dir, "EFI"), efi_backup_dir)
        log(f"{GREEN}Backup criado com sucesso.{NC}")
    except Exception as e:
        log(f"{RED}Erro ao criar o backup: {e}{NC}")
        sys.exit(1)