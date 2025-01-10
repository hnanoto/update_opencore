import os
import sys
from environment import check_environment
from dependencies import check_dependencies
from efi import list_all_efi, get_installed_opencore_version, update_efi, update_boot_files  # Importe update_boot_files
from downloads import download_oc, get_latest_opencore_version, download_hfs_driver
from drivers import update_drivers
from config import add_new_keys_to_config, create_python_script
from validate import validate_config_plist
from backup import backup_efi
from cleanup import cleanup
from logger import log, get_translation, RED, GREEN, YELLOW, NC

def main():
    """Função principal que exibe o menu e executa as ações."""
    check_environment()
    check_dependencies()
    efi_dir = list_all_efi()  # Captura o valor de EFI_DIR

    current_version = get_installed_opencore_version(efi_dir)
    latest_version = get_latest_opencore_version()

    log(f"{get_translation( 'version_not_detected', fallback_to_key=True)}: {current_version}")
    log(f"{get_translation( 'latest_version', fallback_to_key=True)}: {latest_version}")

    # Variável para armazenar a escolha do usuário (RELEASE ou DEBUG)
    build_type = "RELEASE"

    while True:
        print("\nEscolha uma opção:")
        
        menu_options = [
            "update_opencore_release",
            "update_opencore_debug",
            "update_drivers_only",
            "add_new_keys",
            "validate_config_plist",
            "update_boot_files", # Nova opção
            "exit"
        ]

        # Exibe as opções do menu traduzidas, se disponível, se não mostra em inglês
        for i, option in enumerate(menu_options):
            translation = get_translation(option)
            print(f"{i + 1}. {translation}")

        try:
            choice = int(input(f"{get_translation( 'choose_option', fallback_to_key=True)}: "))
        except ValueError:
            log(f"{RED}{get_translation( 'invalid_option')}{NC}")
            continue

        if choice == 1:
            build_type = "RELEASE"
            backup_efi(efi_dir)
            download_oc(build_type)
            update_efi(efi_dir, build_type)
            update_drivers(efi_dir)
            create_python_script()
            cleanup()
            log(f"{GREEN}{get_translation( 'update_opencore_release')}{NC}")
        elif choice == 2:
            build_type = "DEBUG"
            backup_efi(efi_dir)
            download_oc(build_type)
            update_efi(efi_dir, build_type)
            update_drivers(efi_dir)
            create_python_script()
            cleanup()
            log(f"{GREEN}{get_translation( 'update_opencore_debug')}{NC}")
        elif choice == 3:
            backup_efi(efi_dir)
            download_oc(build_type) # Usa a última versão baixada
            update_drivers(efi_dir)
            cleanup()
            log(f"{GREEN}{get_translation( 'update_drivers_only')}{NC}")
        elif choice == 4:
            create_python_script()
            backup_efi(efi_dir)
            download_oc(build_type) # Usa a última versão baixada
            add_new_keys_to_config(efi_dir)
            cleanup()
            log(f"{GREEN}{get_translation( 'new_keys_added')}{NC}")
        elif choice == 5:
            download_oc(build_type) # Usa a última versão baixada
            validate_config_plist(efi_dir)
            cleanup()
        elif choice == 6:
            # Nova opção
            backup_efi(efi_dir)
            download_oc(build_type)
            update_boot_files(efi_dir, build_type)
            cleanup()
            log(f"{GREEN}{get_translation('update_boot_files_success')}{NC}")
        elif choice == 7:
            log(f"{YELLOW}{get_translation( 'exit')}{NC}")
            sys.exit(0)
        else:
            log(f"{RED}{get_translation( 'invalid_option')}{NC}")

if __name__ == "__main__":
    main()