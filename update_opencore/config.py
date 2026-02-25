import os
import subprocess
import plistlib
from logger import log, RED, YELLOW, GREEN, NC

def add_new_keys_recursive(current_dict, sample_dict):
    """Recursively adds new keys from sample_dict to current_dict."""
    for key, value in sample_dict.items():
        if key not in current_dict:
            if not is_warning_key(key) and not is_generic_placeholder_key(key) and key != "PciRoot(0x0)/Pci(0x1b,0x0)":
                log(f"Adicionando nova chave: {key}")
                current_dict[key] = value
            elif key.upper() == "UNLOAD":
                log(f"Adicionando nova chave: {key}")
                current_dict[key] = value
        else:
            if isinstance(value, dict) and isinstance(current_dict[key], dict):
                add_new_keys_recursive(current_dict[key], value)
            elif isinstance(value, list) and isinstance(current_dict[key], list):
                current_dict[key] = add_new_items_to_list(current_dict[key], value, key)

def add_new_items_to_list(current_list, sample_list, parent_key=None):
    """Adds new items from sample_list to current_list, handling dictionaries more intelligently."""
    new_list = current_list[:]

    for sample_item in sample_list:
        if isinstance(sample_item, dict):
            found_similar = False
            for current_item in new_list:
                if isinstance(current_item, dict):
                    if 'Path' in sample_item and 'Path' in current_item and sample_item['Path'] == current_item['Path']:
                        found_similar = True
                        break
                    if 'BundlePath' in sample_item and 'BundlePath' in current_item and sample_item['BundlePath'] == current_item['BundlePath']:
                        found_similar = True
                        break
                    if 'Identifier' in sample_item and 'Identifier' in current_item and sample_item['Identifier'] == current_item['Identifier']:
                        found_similar = True
                        break
                    if 'Comment' in sample_item and 'Comment' in current_item and sample_item['Comment'] == current_item['Comment']:
                        found_similar = True
                        break
                    if parent_key == "PlatformInfo" and "Generic" in current_item and "Generic" in sample_item:
                        found_similar = True
                        break

            if not found_similar:
                if not is_generic_comment_or_placeholder(sample_item):
                    log(f"Adicionando novo item à lista: {sample_item.get('Comment', sample_item.get('Path', sample_item.get('BundlePath', 'Generic')))}")
                    new_list.append(sample_item)
        else:
            if sample_item not in new_list:
                log(f"Adicionando novo item à lista: {sample_item}")
                new_list.append(sample_item)

    return new_list

def is_generic_placeholder_key(key):
    return key.upper() in ("GENERIC")

def is_generic_comment_or_placeholder(item):
    comment = item.get('Comment', '').upper()
    path = item.get('Path', '').upper()
    bundle_path = item.get('BundlePath', '').upper()
    common_placeholders = ["MY CUSTOM", "READ THE COMMENT", "INTEL ETHERNET", "XHC PORTS", "APPLEMCEREPORTER", "MEMORY TESTING"]
    return any(phrase in comment for phrase in common_placeholders) or comment == '' or 'SAMPLE' in comment or 'GENERIC' in path or 'GENERIC' in bundle_path

def is_warning_key(key):
    return key.upper().startswith("#WARNING")

def add_new_keys_to_config(efi_dir):
    """Adiciona novas chaves do Sample.plist ao config.plist."""
    import sys
    log(f"{YELLOW}{get_translation('adding_new_keys', fallback_to_key=True)}{NC}")
    sample_config = os.path.join("OpenCore", "Docs", "Sample.plist")
    current_config = os.path.join(efi_dir, "EFI", "OC", "config.plist")

    if not os.path.isfile(sample_config) or not os.path.isfile(current_config):
        log(f"{RED}Erro: Arquivos de configuração não encontrados.{NC}")
        sys.exit(1)

    try:
        with open(current_config, "rb") as f:
            current_plist = plistlib.load(f)
        with open(sample_config, "rb") as f:
            sample_plist = plistlib.load(f)
    except Exception as e:
        log(f"{RED}Erro ao ler os arquivos plist: {e}{NC}")
        sys.exit(1)

    add_new_keys_recursive(current_plist, sample_plist)

    try:
        with open(current_config, "wb") as f:
            plistlib.dump(current_plist, f)
        log(f"{GREEN}{get_translation('new_keys_added', fallback_to_key=True)}{NC}")
    except Exception as e:
        log(f"{RED}Erro ao salvar o config.plist atualizado: {e}{NC}")
        sys.exit(1)

def get_enabled_drivers(efi_dir):
    """Obtém a lista de drivers habilitados no config.plist usando plistlib."""
    config_plist = os.path.join(efi_dir, "EFI", "OC", "config.plist")

    if not os.path.isfile(config_plist):
        log(f"{RED}Erro: Arquivo config.plist não encontrado em {config_plist}.{NC}")
        sys.exit(1)

    # Carrega o config.plist usando plistlib
    try:
        with open(config_plist, "rb") as f:
            plist_data = plistlib.load(f)
        log(f"{YELLOW}Arquivo config.plist carregado com sucesso usando plistlib.{NC}")
    except Exception as e:
        log(f"{RED}Erro ao carregar config.plist com plistlib: {e}{NC}")
        sys.exit(1)

    # Extrai os drivers habilitados da seção UEFI -> Drivers
    enabled_drivers = []
    try:
        drivers_array = plist_data["UEFI"]["Drivers"]
        log(f"{YELLOW}Lista de drivers (plistlib): {drivers_array}{NC}")

        for item in drivers_array:
            if isinstance(item, str):
                # Se o item é uma string, use a string diretamente como nome do driver.
                driver_name = item
            elif isinstance(item, dict) and item.get("Enabled", False):
                # Se o item é um dicionário, use a chave "Path" como nome do driver.
                driver_name = item.get("Path", "")
            else:
                continue  # Pula itens que não são nem string nem dicionário com "Enabled"

            # Remove a extensão .efi do nome do driver, se presente.
            if driver_name.endswith(".efi"):
                driver_name = driver_name[:-4]

            enabled_drivers.append(driver_name)

    except KeyError as e:
        log(f"{RED}Erro ao acessar a chave UEFI -> Drivers no config.plist: {e}{NC}")
    except Exception as e:
        log(f"{RED}Erro ao extrair drivers do config.plist com plistlib: {e}{NC}")

    log(f"{YELLOW}Drivers habilitados (plistlib): {enabled_drivers}{NC}")
    return enabled_drivers