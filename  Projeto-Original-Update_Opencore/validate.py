import os
import subprocess
from logger import log, RED, YELLOW, GREEN, NC

def validate_config_plist(efi_dir):
    """Valida o config.plist usando ocvalidate."""
    ocvalidate_path = os.path.join("OpenCore", "Utilities", "ocvalidate", "ocvalidate")
    config_plist_path = os.path.join(efi_dir, "EFI", "OC", "config.plist")

    if not os.path.isfile(ocvalidate_path):
        log(f"{RED}Erro: ocvalidate não encontrado em {ocvalidate_path}. Baixe a versão mais recente do OpenCore.{NC}")
        return

    if not os.path.isfile(config_plist_path):
        log(f"{RED}Erro: config.plist não encontrado em {config_plist_path}.{NC}")
        return

    log(f"{YELLOW}Validando config.plist com ocvalidate...{NC}")
    try:
        result = subprocess.run([ocvalidate_path, config_plist_path], capture_output=True, text=True, check=False)
        
        # Verifica se o comando foi executado com sucesso (código de saída 0)
        if result.returncode == 0:
            log(f"{GREEN}Validação do config.plist concluída com sucesso. Saída do ocvalidate:{NC}\n{result.stdout}")
        else:
            log(f"{RED}Erro na validação do config.plist. Saída do ocvalidate:{NC}\n{result.stdout}")

    except subprocess.CalledProcessError as e:
        log(f"{RED}Erro ao executar ocvalidate: {e.stderr}{NC}")