import os
import shutil
from logger import log, RED, YELLOW, GREEN, NC
from downloads import download_hfs_driver
from config import get_enabled_drivers

def update_drivers(efi_dir):
    """Atualiza os drivers na pasta EFI/OC/Drivers e remove os não utilizados."""
    efi_drivers_dir = os.path.join(efi_dir, "EFI", "OC", "Drivers")
    new_drivers_dir = os.path.join("OpenCore", "X64", "EFI", "OC", "Drivers")

    if not os.path.isdir(efi_drivers_dir):
        log(f"{RED}Erro: Pasta de drivers EFI não encontrada em {efi_drivers_dir}.{NC}")
        sys.exit(1)

    enabled_drivers = get_enabled_drivers(efi_dir)
    
    # Adiciona a extensão .efi aos drivers habilitados
    enabled_drivers_with_extension = [
        driver + ".efi" if not driver.endswith(".efi") else driver
        for driver in enabled_drivers
    ]

    log(f"{YELLOW}Atualizando drivers em {efi_drivers_dir}...{NC}")

    # Dicionário para rastrear quais drivers foram processados ou existem na EFI
    processed_drivers = {}

    # Marca todos os drivers habilitados como processados
    for driver in enabled_drivers_with_extension:
        processed_drivers[driver] = True

    # Verifica e baixa o HfsPlus.efi se necessário
    hfsplus_driver = "HfsPlus.efi"
    if hfsplus_driver in enabled_drivers_with_extension and not os.path.exists(os.path.join(efi_drivers_dir, hfsplus_driver)):
        log(f"{YELLOW}Baixando {hfsplus_driver} do repositório OcBinaryData...{NC}")
        download_hfs_driver()
        
        # Verifica se o HfsPlus.efi foi baixado com sucesso antes de tentar copiá-lo
        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), hfsplus_driver)):
            try:
                shutil.copy2(os.path.join(os.path.dirname(os.path.abspath(__file__)), hfsplus_driver), os.path.join(efi_drivers_dir, hfsplus_driver))
                log(f"{GREEN}{hfsplus_driver} copiado para a pasta Drivers da EFI.{NC}")
            except Exception as e:
                log(f"{RED}Erro ao copiar {hfsplus_driver} para a pasta Drivers da EFI: {e}{NC}")
                sys.exit(1)
        else:
            log(f"{RED}Erro: {hfsplus_driver} não foi baixado com sucesso.{NC}")
            sys.exit(1)

    # Atualiza os drivers habilitados
    for new_driver in os.listdir(new_drivers_dir):
        if not new_driver.endswith(".efi"):
            continue

        new_driver_path = os.path.join(new_drivers_dir, new_driver)
        efi_driver_path = os.path.join(efi_drivers_dir, new_driver)

        if new_driver in enabled_drivers_with_extension:
            log(f"{YELLOW}Atualizando {new_driver} (sobrescrevendo)...{NC}")
            try:
                shutil.copy2(new_driver_path, efi_driver_path)
            except Exception as e:
                log(f"{RED}Erro ao atualizar {new_driver}: {e}{NC}")
                sys.exit(1)
        else:
            log(f"{YELLOW}Driver {new_driver} não está habilitado no config.plist. Pulando.{NC}")

    # Remove drivers não utilizados
    log(f"{YELLOW}Removendo drivers não utilizados da pasta {efi_drivers_dir}...{NC}")
    for efi_driver in os.listdir(efi_drivers_dir):
        if efi_driver.endswith(".efi") and efi_driver not in processed_drivers:
            efi_driver_path = os.path.join(efi_drivers_dir, efi_driver)
            log(f"{YELLOW}Removendo driver não utilizado: {efi_driver}{NC}")
            try:
                os.remove(efi_driver_path)
            except Exception as e:
                log(f"{RED}Erro ao remover {efi_driver}: {e}{NC}")
                sys.exit(1)

    log(f"{GREEN}Drivers atualizados e drivers não utilizados removidos com sucesso.{NC}")