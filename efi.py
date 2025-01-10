import os
import subprocess
import shutil
import sys
import time
from logger import log, get_translation, RED, YELLOW, GREEN, NC

# Definindo EFI_DIR como global
EFI_DIR = ""

def list_all_efi():
    """Lista todas as partições EFI e aguarda até que a partição selecionada seja montada."""
    global EFI_DIR
    log(f"{YELLOW}{get_translation('environment_check')}{NC}")
    if not sys.platform.startswith("darwin"):
        log(f"{RED}{get_translation('environment_error_macos')}{NC}")
        sys.exit(1)
    if os.geteuid() != 0:
        log(f"{YELLOW}{get_translation('environment_error_root')}{NC}")
        os.execvp("sudo", ["sudo"] + sys.argv)
    log(f"{GREEN}{get_translation('environment_success')}{NC}")
    
    log(f"{YELLOW}{get_translation('dependencies_check')}{NC}")
    dependencies = ["curl", "unzip", "python3"]
    for cmd in dependencies:
        if not shutil.which(cmd):
            log(f"{RED}{get_translation('dependency_not_found', True).format(cmd=cmd)}{NC}")
            if cmd == "python3":
                log(f"{YELLOW}{get_translation('python3_needed')}{NC}")
            sys.exit(1)
    log(f"{GREEN}{get_translation('dependencies_success')}{NC}")

    log(f"{YELLOW}Localizando todas as partições EFI no sistema...{NC}")
    try:
        diskutil_output = subprocess.check_output(["diskutil", "list"]).decode("utf-8")
        all_efis = [line.split()[-1] for line in diskutil_output.splitlines() if "EFI" in line]
    except subprocess.CalledProcessError:
        log(f"{RED}{get_translation('efi_detect_error')}{NC}")
        sys.exit(1)

    if not all_efis:
        log(f"{RED}{get_translation('no_efi_found')}{NC}")
        sys.exit(1)

    log(f"{YELLOW}Partições EFI detectadas:{NC}")
    for i, efi_part in enumerate(all_efis):
        log(f"{i + 1}. {efi_part}")

    while True:
        try:
            efi_choice = int(input(f"{get_translation('select_efi')}: ")) - 1
            if 0 <= efi_choice < len(all_efis):
                efi_part = all_efis[efi_choice]
                break
            else:
                log(f"{RED}{get_translation('invalid_option')}{NC}")
        except ValueError:
            log(f"{RED}{get_translation('invalid_option')}{NC}")

    while True:
        try:
            diskutil_info = subprocess.check_output(["diskutil", "info", efi_part]).decode("utf-8")
            efi_dir_line = [line.strip() for line in diskutil_info.splitlines() if "Mount Point" in line]
            if efi_dir_line:
                efi_dir = efi_dir_line[0].split(":")[-1].strip()
            else:
                efi_dir = ""
        except subprocess.CalledProcessError:
            log(f"{RED}Erro: Falha ao executar 'diskutil info {efi_part}'.{NC}")
            sys.exit(1)

        EFI_DIR = efi_dir
        log(f"{get_translation('selected_efi')} {EFI_DIR}")

        if efi_dir:
            log(f"{GREEN}Partição EFI montada com sucesso. Continuando...{NC}")
            break  # Sai do loop se a partição estiver montada
        else:
            log(f"{RED}{get_translation('efi_partition_error')}{NC}")
            log(f"{YELLOW}{get_translation('mount_manualy')}{NC}")
            log(f"{YELLOW}{get_translation('wait_5_seconds')}{NC}")
            time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente

    return efi_dir

def get_installed_opencore_version(efi_dir):
    """Detecta a versão do OpenCore instalada na EFI."""
    opencore_efi_path = os.path.join(efi_dir, "EFI", "OC", "OpenCore.efi")
    if os.path.exists(opencore_efi_path):
        try:
            # Executa o comando strings para buscar a versão do OpenCore.efi
            result = subprocess.run(
                ["strings", opencore_efi_path],
                capture_output=True,
                text=True,
                check=True
            )
            # Busca pela linha que contém a versão
            for line in result.stdout.splitlines():
                if "OpenCore.efi" in line:
                    version = line.split()[-2]
                    return version
        except subprocess.CalledProcessError as e:
            log(f"{RED}Erro ao detectar a versão do OpenCore: {e}{NC}")
    return get_translation('version_not_detected', fallback_to_key=True)

def update_efi(efi_dir, build_type="RELEASE"):
    """Atualiza os arquivos EFI, mas não a pasta Drivers."""
    efi_source_dir = os.path.join("OpenCore", "X64", "EFI")
    efi_target_dir = os.path.join(efi_dir, "EFI")

    if not os.path.isdir(efi_source_dir):
        log(f"{RED}{get_translation('source_folder_not_found').format(efi_source_dir=efi_source_dir)}{NC}")
        sys.exit(1)

    log(f"{YELLOW}{get_translation('updating_efi_files').format(efi_target_dir=efi_target_dir)}{NC}")
    try:
        # Copia todos os arquivos e pastas, exceto a pasta Drivers
        for item in os.listdir(efi_source_dir):
            source_item = os.path.join(efi_source_dir, item)
            target_item = os.path.join(efi_target_dir, item)

            if item == "Drivers":
                log(f"{YELLOW}{get_translation('pulled_drivers_folder')}{NC}")
                continue

            if os.path.isdir(source_item):
                shutil.copytree(source_item, target_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, target_item)
        log(f"{GREEN}{get_translation('update_efi_success')}{NC}")
    except Exception as e:
        log(f"{RED}{get_translation('update_efi_error')}: {e}{NC}")
        sys.exit(1)

def update_boot_files(efi_dir, build_type="RELEASE"):
    """Atualiza os arquivos BOOTx64.efi e OpenCore.efi na EFI."""
    source_dir = os.path.join("OpenCore", "X64")
    boot_efi_source = os.path.join(source_dir, "EFI", "BOOT", "BOOTx64.efi")
    opencore_efi_source = os.path.join(source_dir, "EFI", "OC", "OpenCore.efi")

    boot_efi_target = os.path.join(efi_dir, "EFI", "BOOT", "BOOTx64.efi")
    opencore_efi_target = os.path.join(efi_dir, "EFI", "OC", "OpenCore.efi")

    log(f"{YELLOW}Atualizando BOOTx64.efi e OpenCore.efi em {efi_dir}/EFI...{NC}")
    try:
        shutil.copy2(boot_efi_source, boot_efi_target)
        log(f"{GREEN}BOOTx64.efi atualizado com sucesso.{NC}")
        shutil.copy2(opencore_efi_source, opencore_efi_target)
        log(f"{GREEN}OpenCore.efi atualizado com sucesso.{NC}")
    except Exception as e:
        log(f"{RED}Erro ao atualizar arquivos de boot: {e}{NC}")
        sys.exit(1)
