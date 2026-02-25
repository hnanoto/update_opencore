import json

new_en = {
    "efi_selected_success": "Selected EFI partition: {efi_dir}",
    "efi_mounted_success": "EFI partition mounted successfully and contains a valid OpenCore installation. Continuing...",
    "efi_invalid_error": "Error: The selected EFI partition ({efi_dir}) does not appear to contain a valid OpenCore installation.",
    "efi_mount_auto_try": "Attempting to mount EFI partition ({efi_part}) automatically...",
    "efi_mount_wait": "Waiting 5 seconds...",
    "efi_diskutil_error": "Error: Failed to execute 'diskutil info {efi_part}'.",
    "detect_oc_version_error": "Error detecting OpenCore version: {e}",
    "updating_boot_efi_msg": "Updating BOOTx64.efi and OpenCore.efi in {efi_dir}/EFI...",
    "bootx64_updated": "BOOTx64.efi updated successfully.",
    "opencore_efi_updated": "OpenCore.efi updated successfully.",
    "boot_files_error": "Error updating boot files: {e}"
}

new_pt = {
    "efi_selected_success": "Partição EFI selecionada: {efi_dir}",
    "efi_mounted_success": "Partição EFI montada com sucesso e contém uma instalação do OpenCore. Continuando...",
    "efi_invalid_error": "Erro: A partição EFI selecionada ({efi_dir}) não parece conter uma instalação válida do OpenCore.",
    "efi_mount_auto_try": "Tentando montar a partição EFI ({efi_part}) automaticamente...",
    "efi_mount_wait": "Aguardando 5 segundos...",
    "efi_diskutil_error": "Erro: Falha ao executar 'diskutil info {efi_part}'.",
    "detect_oc_version_error": "Erro ao detectar a versão do OpenCore: {e}",
    "updating_boot_efi_msg": "Atualizando BOOTx64.efi e OpenCore.efi em {efi_dir}/EFI...",
    "bootx64_updated": "BOOTx64.efi atualizado com sucesso.",
    "opencore_efi_updated": "OpenCore.efi atualizado com sucesso.",
    "boot_files_error": "Erro ao atualizar arquivos de boot: {e}"
}

def update_json(file, new_data):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for k, v in new_data.items():
            if k not in data or data[k] != v:
                data[k] = v
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error updating {file}: {e}")

update_json("update_opencore/translations/en.json", new_en)
update_json("update_opencore/translations/pt-BR.json", new_pt)
print("Translations updated round 3.")
