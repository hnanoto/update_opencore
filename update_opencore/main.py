#!/usr/bin/env python3
import os
import sys
from typing import NoReturn

from environment import check_environment
from dependencies import check_dependencies
from efi import list_all_efi, get_installed_opencore_version, update_efi, update_boot_files
from downloads import download_oc, get_latest_opencore_version, download_hfs_driver
from drivers import update_drivers
from config import add_new_keys_to_config
from validate import validate_config_plist
from backup import backup_efi
from cleanup import cleanup
from logger import log, get_translation, RED, GREEN, YELLOW, NC

def main() -> None:
    """Função principal que exibe o menu e executa as ações em looping gracioso."""
    check_environment()
    check_dependencies()
    efi_dir: str = list_all_efi()  # Captura o valor de EFI_DIR

    current_version: str = get_installed_opencore_version(efi_dir)
    latest_version: str = get_latest_opencore_version()

    log(f"{get_translation('version_not_detected', fallback_to_key=True)}: {current_version}")
    log(f"{get_translation('latest_version', fallback_to_key=True)}: {latest_version}")

    build_type: str = "RELEASE"

    while True:
        pre_release: bool = False
        print(get_translation('choose_option_menu', fallback_to_key=True))
        
        menu_options: list[str] = [
            "update_opencore_release",
            "update_opencore_debug",
            "update_drivers_only",
            "add_new_keys",
            "validate_config_plist",
            "update_boot_files",
            "update_opencore_pre_release",
            "exit"
        ]

        for i, option in enumerate(menu_options):
            translation: str = get_translation(option)
            print(f"{i + 1}. {translation}")

        try:
            choice_input: str = input(f"{get_translation('choose_option', fallback_to_key=True)}: ")
            choice: int = int(choice_input)
        except ValueError:
            log(f"{RED}{get_translation('invalid_option', fallback_to_key=True)}{NC}")
            continue

        if choice == 8:
            log(f"{YELLOW}{get_translation('exit', fallback_to_key=True)}{NC}")
            sys.exit(0)

        # Trata erros intencionais sem crachar o app
        try:
            if choice == 1:
                build_type = "RELEASE"
                backup_efi(efi_dir)
                if download_oc(build_type, pre_release):
                    update_efi(efi_dir, build_type)
                    update_drivers(efi_dir)
                    cleanup()
                    log(f"{GREEN}{get_translation('update_opencore_release', fallback_to_key=True)}{NC}")
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            elif choice == 2:
                build_type = "DEBUG"
                backup_efi(efi_dir)
                if download_oc(build_type, pre_release):
                    update_efi(efi_dir, build_type)
                    update_drivers(efi_dir)
                    cleanup()
                    log(f"{GREEN}{get_translation('update_opencore_debug', fallback_to_key=True)}{NC}")
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            elif choice == 3:
                backup_efi(efi_dir)
                if download_oc(build_type, pre_release):
                    update_drivers(efi_dir)
                    cleanup()
                    log(f"{GREEN}{get_translation('update_drivers_only', fallback_to_key=True)}{NC}")
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            elif choice == 4:
                backup_efi(efi_dir)
                if download_oc(build_type, pre_release):
                    add_new_keys_to_config(efi_dir)
                    cleanup()
                    log(f"{GREEN}{get_translation('new_keys_added', fallback_to_key=True)}{NC}")
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            elif choice == 5:
                if download_oc(build_type, pre_release):
                    validate_config_plist(efi_dir)
                    cleanup()
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            elif choice == 6:
                backup_efi(efi_dir)
                if download_oc(build_type, pre_release):
                    update_boot_files(efi_dir, build_type)
                    cleanup()
                    log(f"{GREEN}{get_translation('update_boot_files_success', fallback_to_key=True)}{NC}")
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            elif choice == 7:
                build_type = input(get_translation('oc_pre_release_prompt', fallback_to_key=True)).upper()
                pre_release = True
                backup_efi(efi_dir)
                if download_oc(build_type, pre_release):
                    update_efi(efi_dir, build_type)
                    update_drivers(efi_dir)
                    cleanup()
                    log(f"{GREEN}{get_translation('oc_pre_release_success', fallback_to_key=True)}{NC}")
                else:
                    log(f"{RED}{get_translation('download_oc_fail_log', fallback_to_key=True)}{NC}")
            
            else:
                log(f"{RED}{get_translation('invalid_option', fallback_to_key=True)}{NC}")

        except SystemExit as e:
            # Handles unexpected logic exits without blowing up the shell
            if e.code == 0:
                raise
            log(f"\n{RED}Operation aborted safely! returning to main menu...{NC}")
            input(f"{YELLOW}Press ENTER to continue...{NC}")
            continue
            
        except Exception as general_error:
            # A completely broken OS runtime error (e.g. disk fully unmounted during loop)
            log(f"\n{RED}Critical Runtime Error: {general_error}{NC}")
            input(f"{YELLOW}Press ENTER to restart menu...{NC}")
            continue

if __name__ == "__main__":
    main()