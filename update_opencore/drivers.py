import os
import shutil
import sys
from datetime import datetime
from logger import log, RED, YELLOW, GREEN, NC
from downloads import download_hfs_driver
from config import get_enabled_drivers

def get_drivers_by_modification_time(drivers_dir):
    """Retorna lista de drivers ordenados por data de modificação (mais antigos primeiro)."""
    drivers = []
    for filename in os.listdir(drivers_dir):
        if filename.endswith(".efi"):
            file_path = os.path.join(drivers_dir, filename)
            mod_time = os.path.getmtime(file_path)
            drivers.append((filename, mod_time, file_path))
    
    # Ordena por data de modificação (mais antigos primeiro)
    drivers.sort(key=lambda x: x[1])
    return drivers

def update_hfsplus_driver(efi_drivers_dir, enabled_drivers_with_extension):
    """Atualiza o HfsPlus.efi se estiver habilitado."""
    hfsplus_driver = "HfsPlus.efi"
    
    if hfsplus_driver in enabled_drivers_with_extension:
        log(f"{YELLOW}🔄 Verificando {hfsplus_driver} (driver externo)...{NC}")
        
        # Sempre baixa a versão mais recente do HfsPlus.efi
        log(f"{YELLOW}📥 Baixando {hfsplus_driver} do repositório OcBinaryData...{NC}")
        download_hfs_driver()
        
        # Verifica se o HfsPlus.efi foi baixado com sucesso
        local_hfsplus_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), hfsplus_driver)
        efi_hfsplus_path = os.path.join(efi_drivers_dir, hfsplus_driver)
        
        if os.path.exists(local_hfsplus_path):
            try:
                # Sempre copia (atualiza) o HfsPlus.efi
                shutil.copy2(local_hfsplus_path, efi_hfsplus_path)
                
                # Verifica se a cópia foi bem-sucedida
                if os.path.exists(efi_hfsplus_path):
                    file_size = os.path.getsize(efi_hfsplus_path)
                    log(f"{GREEN}✅ {hfsplus_driver} atualizado com sucesso ({file_size} bytes).{NC}")
                    return True
                else:
                    log(f"{RED}❌ Erro: {hfsplus_driver} não foi copiado corretamente.{NC}")
                    return False
            except Exception as e:
                log(f"{RED}❌ Erro ao copiar {hfsplus_driver}: {e}{NC}")
                return False
        else:
            log(f"{RED}❌ Erro: {hfsplus_driver} não foi baixado com sucesso.{NC}")
            return False
    else:
        log(f"{YELLOW}⏭️ {hfsplus_driver} não está habilitado no config.plist. Pulando.{NC}")
        return True

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

    # Atualiza o HfsPlus.efi primeiro (driver externo)
    hfsplus_success = update_hfsplus_driver(efi_drivers_dir, enabled_drivers_with_extension)
    if not hfsplus_success:
        log(f"{RED}❌ Falha na atualização do HfsPlus.efi. Abortando.{NC}")
        sys.exit(1)

    # Obtém drivers ordenados por data de modificação (excluindo HfsPlus.efi)
    sorted_drivers = get_drivers_by_modification_time(new_drivers_dir)
    
    # Filtra apenas drivers que não são HfsPlus.efi (já foi tratado)
    sorted_drivers = [d for d in sorted_drivers if d[0] != "HfsPlus.efi"]
    
    log(f"{YELLOW}Atualizando {len(sorted_drivers)} drivers do OpenCore em ordem de modificação...{NC}")
    
    # Atualiza os drivers habilitados em ordem de modificação
    updated_count = 0
    for i, (new_driver, mod_time, new_driver_path) in enumerate(sorted_drivers, 1):
        efi_driver_path = os.path.join(efi_drivers_dir, new_driver)
        mod_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')

        if new_driver in enabled_drivers_with_extension:
            log(f"{YELLOW}[{i}/{len(sorted_drivers)}] Atualizando {new_driver} (modificado em {mod_date})...{NC}")
            try:
                shutil.copy2(new_driver_path, efi_driver_path)
                log(f"{GREEN}✅ {new_driver} atualizado com sucesso.{NC}")
                updated_count += 1
            except Exception as e:
                log(f"{RED}❌ Erro ao atualizar {new_driver}: {e}{NC}")
                sys.exit(1)
        else:
            log(f"{YELLOW}[{i}/{len(sorted_drivers)}] Driver {new_driver} não está habilitado no config.plist. Pulando.{NC}")

    # Pergunta se deseja remover drivers não utilizados
    not_used_drivers = [d for d in os.listdir(efi_drivers_dir) if d.endswith(".efi") and d not in processed_drivers]
    removed_count = 0
    
    if not_used_drivers:
        log(f"{YELLOW}🔍 Foram encontrados {len(not_used_drivers)} drivers na pasta EFI que NÃO estão habilitados no config.plist.{NC}")
        for d in not_used_drivers:
            log(f"{YELLOW}   - {d}{NC}")
        
        while True:
            choice = input(f"{YELLOW}Deseja remover estes drivers permanentemente? (y/n): {NC}").lower()
            if choice in ['y', 'yes', 's', 'sim']:
                log(f"{YELLOW}Removendo drivers não utilizados...{NC}")
                for efi_driver in not_used_drivers:
                    efi_driver_path = os.path.join(efi_drivers_dir, efi_driver)
                    log(f"{YELLOW}🗑️ Removendo driver: {efi_driver}{NC}")
                    try:
                        os.remove(efi_driver_path)
                        removed_count += 1
                    except Exception as e:
                        log(f"{RED}❌ Erro ao remover {efi_driver}: {e}{NC}")
                        sys.exit(1)
                break
            elif choice in ['n', 'no', 'nao', 'não']:
                log(f"{GREEN}Mantendo os drivers não utilizados.{NC}")
                break
            else:
                log(f"{RED}Opção inválida.{NC}")

    # Calcula total de drivers atualizados (incluindo HfsPlus.efi)
    total_updated = updated_count
    if "HfsPlus.efi" in enabled_drivers_with_extension:
        total_updated += 1

    log(f"{GREEN}✅ Drivers atualizados com sucesso!")
    log(f"{GREEN}📊 Resumo: {total_updated} drivers atualizados ({updated_count} do OpenCore + HfsPlus.efi), {removed_count} drivers removidos.{NC}")