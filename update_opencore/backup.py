import os
import shutil
from datetime import datetime
from logger import log, get_translation, RED, YELLOW, GREEN, NC
import sys

def backup_efi(efi_dir):
    """Cria backup da EFI, perguntando ao usuário se ele deseja prosseguir."""
    
    def confirm_backup():
        """Pergunta ao usuário se ele deseja fazer um backup da EFI."""
        while True:
            choice = input(f"{get_translation('confirm_backup')} (y/n): ").lower()
            if choice in ['y', 'yes', 's', 'sim']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                log(f"{RED}{get_translation('invalid_option')}{NC}")

    if not confirm_backup():
        log(f"{YELLOW}{get_translation('backup_cancelled', fallback_to_key=True)}{NC}")
        return  # Sai da função se o usuário não quiser fazer backup

    backup_dir = os.path.join(efi_dir, f"EFI-Backup-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    log(f"{YELLOW}{get_translation('creating_backup', fallback_to_key=True).format(backup_dir=backup_dir)}{NC}")
    try:
        shutil.copytree(os.path.join(efi_dir, "EFI"), backup_dir)
        log(f"{GREEN}{get_translation('backup_success', fallback_to_key=True)}{NC}")
        
        # Rotacionar backups: manter apenas os 2 mais recentes
        backups = [d for d in os.listdir(efi_dir) if d.startswith("EFI-Backup-") and os.path.isdir(os.path.join(efi_dir, d))]
        backups.sort()
        if len(backups) > 2:
            log(f"{YELLOW}{get_translation('removing_old_backups', fallback_to_key=True)}{NC}")
            for old_backup in backups[:-2]:
                old_backup_path = os.path.join(efi_dir, old_backup)
                log(f"{YELLOW}{get_translation('backup_limit_deleted', fallback_to_key=True).format(folder=old_backup_path)}{NC}")
                shutil.rmtree(old_backup_path)
    except Exception as e:
        log(f"{RED}{get_translation('backup_error', fallback_to_key=True).format(e=e)}{NC}")
        sys.exit(1)
