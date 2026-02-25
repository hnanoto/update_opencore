import os
import subprocess
import shutil
import sys
import time
from logger import log, get_translation, RED, YELLOW, GREEN, NC

# Definindo EFI_DIR como global
EFI_DIR = ""

def list_all_efi():
    """Lista todas as partições EFI e aguarda até que a partição selecionada seja montada e validada."""
    global EFI_DIR
    EFI_DIR = ""  # Reseta EFI_DIR

    log(f"{YELLOW}Localizando todas as partições EFI no sistema...{NC}")
    try:
        diskutil_output = subprocess.check_output(["diskutil", "list"]).decode("utf-8")
        raw_parts = []
        for line in diskutil_output.splitlines():
            s = line.split()
            if s and "disk" in s[-1] and "s" in s[-1]:
                raw_parts.append(s[-1])
    except subprocess.CalledProcessError:
        log(f"{RED}{get_translation('efi_detect_error')}{NC}")
        sys.exit(1)

    all_efis = []
    log(f"{YELLOW}Partições FAT32/EFI detectadas (HDs e Pendrives):{NC}")
    
    import re
    count = 1
    for part in raw_parts:
        if not part.startswith("disk"):
            continue
            
        # Extrai corretamente o disco raiz (ex: disk0s1 -> disk0, disk11s3s1 -> disk11)
        parent_disk_match = re.search(r'^(disk\d+)', part)
        parent_disk = parent_disk_match.group(1) if parent_disk_match else part
        
        disk_name = "Disco Desconhecido"
        is_fat32 = ""
        is_valid = False
        volume_name = ""
        
        try:
            # Checa se a partição é FAT32 ou EFI, omitindo erros se disco ilegível
            part_info = subprocess.check_output(["diskutil", "info", part], stderr=subprocess.DEVNULL).decode("utf-8")
            part_info_lower = part_info.lower()
            if "fat32" in part_info_lower or "ms-dos" in part_info_lower or "efi" in part_info_lower:
                is_fat32 = " (FAT32)"
                is_valid = True
                
                # Extrai o "Volume Name" real da partição (ex: TESTE CLOVER, UNTITLED)
                v_lines = [l.strip() for l in part_info.splitlines() if "Volume Name:" in l]
                if v_lines:
                    v_name = v_lines[0].split(":", 1)[1].strip()
                    if v_name and v_name != "Not applicable (no file system)" and v_name != "Not applicable (not mounted)":
                        volume_name = f" [{v_name}]"
                
            if is_valid:
                # Recupera o nome físico de hardware do disco pai (ex: SanDisk, WD Black)
                try:
                    parent_info = subprocess.check_output(["diskutil", "info", parent_disk], stderr=subprocess.DEVNULL).decode("utf-8")
                    media_name = [l.strip() for l in parent_info.splitlines() if "Device / Media Name:" in l]
                    if media_name:
                        disk_name = media_name[0].split(":", 1)[1].strip()
                except Exception:
                    pass
                
                log(f"{count}. {part} - {disk_name}{volume_name}{is_fat32}")
                all_efis.append(part)
                count += 1
        except Exception:
            pass

    if not all_efis:
        log(f"{RED}Nenhuma partição FAT32 ou arquivo EFI foi encontrada no sistema.{NC}")
        sys.exit(1)

    while True:
        try:
            efi_choice = int(input(f"{get_translation('select_efi')}: ")) - 1
            if 0 <= efi_choice < len(all_efis):
                efi_part = all_efis[efi_choice]
                # Verifica se a partição selecionada está montada
                while True:
                    efi_dir = "" # Inicializa efi_dir dentro do loop externo, antes do loop interno while True
                    try:
                        diskutil_info = subprocess.check_output(["diskutil", "info", efi_part]).decode("utf-8")
                        efi_dir_line = [line.strip() for line in diskutil_info.splitlines() if "Mount Point" in line]
                        if efi_dir_line:
                            efi_dir = efi_dir_line[0].split(":")[-1].strip()

                        if efi_dir:
                            # Verifica se a EFI é válida
                            efi_path = os.path.join(efi_dir, "EFI")
                            if os.path.isdir(efi_path) and 'OC' in os.listdir(efi_path) and any(fname.endswith('.efi') for fname in os.listdir(os.path.join(efi_path, 'OC', 'Drivers'))):
                                EFI_DIR = efi_dir
                                log(f"Partição EFI selecionada: {EFI_DIR}")
                                log(f"{GREEN}Partição EFI montada com sucesso e contém uma instalação do OpenCore. Continuando...{NC}")
                                return EFI_DIR  # Retorna o caminho da EFI válida
                            else:
                                log(f"{RED}Erro: A partição EFI selecionada ({efi_dir}) não parece conter uma instalação válida do OpenCore.{NC}")
                                # Sai do loop interno para solicitar nova seleção de partição se a EFI não for válida
                                break
                        else:
                            log(f"{YELLOW}Tentando montar a partição EFI ({efi_part}) automaticamente...{NC}")
                            try:
                                subprocess.run(["diskutil", "mount", efi_part], check=True, capture_output=True)
                                time.sleep(1) # Aguarda o sistema registrar a montagem
                                continue
                            except subprocess.CalledProcessError:
                                log(f"{RED}{get_translation('efi_partition_error')}{NC}")
                                log(f"{YELLOW}{get_translation('mount_manualy')}{NC}")
                                log(f"{YELLOW}Aguardando 5 segundos...{NC}")
                                time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
                    except subprocess.CalledProcessError:
                        log(f"{RED}Erro: Falha ao executar 'diskutil info {efi_part}'.{NC}")
                        sys.exit(1)
            else:
                log(f"{RED}{get_translation('invalid_option')}{NC}")
        except ValueError:
            log(f"{RED}{get_translation('invalid_option')}{NC}")

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