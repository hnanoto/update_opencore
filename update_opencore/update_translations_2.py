import json

new_en = {
    "backup_cancelled": "Backup cancelled by the user.",
    "creating_backup": "Creating backup at {backup_dir}...",
    "backup_success": "Backup successfully created.",
    "removing_old_backups": "Cleaning up older backups to save space...",
    "backup_error": "Error creating or rotating backup: {e}",
    "unused_drivers_prompt": "Found {length} unused drivers. Do you want to review them?",
    "prompt_delete_driver": "List of unused drivers:",
    "removing_driver": "Removing unused driver: {driver}",
    "driver_remove_error": "Error removing {driver}: {e}"
}

new_pt = {
    "backup_cancelled": "Backup cancelado pelo usuário.",
    "creating_backup": "Criando backup em {backup_dir}...",
    "backup_success": "Backup criado com sucesso.",
    "removing_old_backups": "Removendo backups antigos para economizar espaço...",
    "backup_error": "Erro ao criar ou rotacionar o backup: {e}",
    "unused_drivers_prompt": "Encontrados {length} drivers não utilizados. Deseja revisá-los?",
    "prompt_delete_driver": "Lista de drivers não utilizados:",
    "removing_driver": "Removendo driver não utilizado: {driver}",
    "driver_remove_error": "Erro ao remover {driver}: {e}"
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
print("Translations updated again.")
