import os
import sys
from environment import check_environment
from dependencies import check_dependencies
from efi import list_all_efi, get_installed_opencore_version, update_efi
from downloads import download_oc, get_latest_opencore_version, download_hfs_driver
from drivers import update_drivers
from config import add_new_keys_to_config, create_python_script
from validate import validate_config_plist
from backup import backup_efi
from cleanup import cleanup
from logger import log, RED, GREEN, YELLOW, NC

def main():
    """Função principal que exibe o menu e executa as ações."""
    check_environment()
    check_dependencies()
    efi_dir = list_all_efi()  # Captura o valor de EFI_DIR

    current_version = get_installed_opencore_version(efi_dir)
    latest_version = get_latest_opencore_version()

    log(f"Versão atual do OpenCore (detectada): {current_version}")
    log(f"Versão mais recente do OpenCore: {latest_version}")

    while True:
        print("\nEscolha uma opção:")
        print("1. Atualizar o OpenCore (RELEASE)")
        print("2. Atualizar o OpenCore (DEBUG)")
        print("3. Atualizar apenas drivers")
        print("4. Adicionar novas chaves ao config.plist")
        print("5. Validar config.plist")
        print("6. Sair")

        try:
            choice = int(input("Opção: "))
        except ValueError:
            log(f"{RED}Entrada inválida. Digite um número.{NC}")
            continue

        if choice == 1:
            backup_efi(efi_dir)
            download_oc("RELEASE")
            update_efi(efi_dir, "RELEASE")
            update_drivers(efi_dir)
            create_python_script()
            cleanup()
            log(f"{GREEN}OpenCore (RELEASE) atualizado com sucesso!{NC}")
        elif choice == 2:
            backup_efi(efi_dir)
            download_oc("DEBUG")
            update_efi(efi_dir, "DEBUG")
            update_drivers(efi_dir)
            create_python_script()
            cleanup()
            log(f"{GREEN}OpenCore (DEBUG) atualizado com sucesso!{NC}")
        elif choice == 3:
            backup_efi(efi_dir)
            download_oc("RELEASE")
            update_drivers(efi_dir)
            cleanup()
            log(f"{GREEN}Drivers atualizados com sucesso!{NC}")
        elif choice == 4:
            create_python_script()
            backup_efi(efi_dir)
            download_oc("RELEASE")
            add_new_keys_to_config(efi_dir)
            cleanup()
            log(f"{GREEN}Novas chaves adicionadas ao config.plist!{NC}")
        elif choice == 5:
            download_oc("RELEASE")
            validate_config_plist(efi_dir)
            cleanup()
        elif choice == 6:
            log(f"{YELLOW}Saindo...{NC}")
            sys.exit(0)
        else:
            log(f"{RED}Opção inválida. Tente novamente.{NC}")

if __name__ == "__main__":
    main()