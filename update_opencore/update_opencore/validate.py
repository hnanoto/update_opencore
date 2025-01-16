import os
import subprocess
from logger import log, RED, YELLOW, GREEN, NC, get_translation  # Importe get_translation

def validate_config_plist(efi_dir):
    """Valida o config.plist usando ocvalidate."""
    ocvalidate_path = os.path.join("OpenCore", "Utilities", "ocvalidate", "ocvalidate")
    config_plist_path = os.path.join(efi_dir, "EFI", "OC", "config.plist")

    if not os.path.isfile(ocvalidate_path):
        log(f"{RED}{get_translation('ocvalidate_path_error', True).format(ocvalidate_path=ocvalidate_path)}{NC}")
        return

    if not os.path.isfile(config_plist_path):
        log(f"{RED}{get_translation('config_plist_path_error', True).format(config_plist_path=config_plist_path)}{NC}")
        return

    log(f"{YELLOW}{get_translation('validating_config_plist', True)}{NC}")
    try:
        result = subprocess.run([ocvalidate_path, config_plist_path], capture_output=True, text=True, check=False)

        # Exibe a saída do ocvalidate sem tradução
        print(result.stdout)

        # Verifica se o comando foi executado com sucesso (código de saída 0)
        if result.returncode == 0:
            log(f"{GREEN}{get_translation('validation_success', True)}{NC}")
        else:
            log(f"{RED}{get_translation('validation_error', True)}{NC}")

    except subprocess.CalledProcessError as e:
        log(f"{RED}{get_translation('ocvalidate_execution_error', True)} {e.stderr}{NC}")