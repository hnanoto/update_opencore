import os
import subprocess
import shutil  # Importando o módulo shutil
import sys  # Importando o módulo sys
from logger import log, RED, YELLOW, GREEN, NC

def list_all_efi():
    """Lista todas as partições EFI."""
    log(f"{YELLOW}Localizando todas as partições EFI no sistema...{NC}")
    try:
        diskutil_output = subprocess.check_output(["diskutil", "list"]).decode("utf-8")
        all_efis = [line.split()[-1] for line in diskutil_output.splitlines() if "EFI" in line]
    except subprocess.CalledProcessError:
        log(f"{RED}Erro: Falha ao executar 'diskutil list'.{NC}")
        sys.exit(1)

    if not all_efis:
        log(f"{RED}Erro: Nenhuma partição EFI encontrada.{NC}")
        sys.exit(1)

    log("Partições EFI detectadas:")
    for i, efi_part in enumerate(all_efis):
        log(f"{i + 1}. {efi_part}")

    while True:
        try:
            efi_choice = int(input(f"Selecione o número da partição EFI que deseja usar: ")) - 1
            if 0 <= efi_choice < len(all_efis):
                efi_part = all_efis[efi_choice]
                break
            else:
                log(f"{RED}Seleção inválida. Tente novamente.{NC}")
        except ValueError:
            log(f"{RED}Entrada inválida. Digite um número.{NC}")

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

    if not efi_dir:
        log(f"{RED}Erro: A partição EFI selecionada não está montada.{NC}")
        log(f"{YELLOW}Monte a EFI manualmente e execute o script novamente.{NC}")
        sys.exit(1)

    log(f"Partição EFI selecionada: {efi_dir}")
    return efi_dir  # Retorna o caminho da EFI

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
    return "Não detectada"

def update_efi(efi_dir, build_type="RELEASE"):
    """Atualiza os arquivos EFI, mas não a pasta Drivers."""
    efi_source_dir = os.path.join("OpenCore", "X64", "EFI")
    efi_target_dir = os.path.join(efi_dir, "EFI")

    if not os.path.isdir(efi_source_dir):
        log(f"{RED}Erro: Pasta EFI de origem não encontrada em {efi_source_dir}.{NC}")
        sys.exit(1)

    log(f"{YELLOW}Atualizando arquivos EFI em {efi_target_dir}...{NC}")
    try:
        # Copia todos os arquivos e pastas, exceto a pasta Drivers
        for item in os.listdir(efi_source_dir):
            source_item = os.path.join(efi_source_dir, item)
            target_item = os.path.join(efi_target_dir, item)

            if item == "Drivers":
                log(f"{YELLOW}Pulando a pasta Drivers conforme instruído.{NC}")
                continue

            if os.path.isdir(source_item):
                shutil.copytree(source_item, target_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, target_item)
        log(f"{GREEN}Arquivos EFI atualizados com sucesso, exceto a pasta Drivers.{NC}")
    except Exception as e:
        log(f"{RED}Erro ao atualizar arquivos EFI: {e}{NC}")
        sys.exit(1)