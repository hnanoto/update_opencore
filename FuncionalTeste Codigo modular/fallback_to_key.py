from datetime import datetime
import os
import json
import locale

# Cores para feedback visual
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0;m"  # Sem cor

# Arquivo de log
LOGFILE = f"update_opencore_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

def get_system_language():
    """Detecta o idioma preferido do usuário usando a biblioteca locale."""
    try:
        lang, encoding = locale.getlocale()
        if lang:
            return lang
        else:
            return "en"  # Inglês como padrão se não for detectado
    except Exception as e:
        log(f"{RED}Erro ao detectar o idioma do sistema: {e}{NC}")
        return "en"

def log(message):
    """Registra a mensagem no arquivo de log e a imprime na tela."""
    with open(LOGFILE, "a") as logfile:
        logfile.write(message + "\n")
    print(message)

def get_translation(key, fallback_to_key=True):
    # ... (código da função) ...

    # Se não encontrar a tradução e fallback_to_key for True, tenta o inglês
    if fallback_to_key:
        try:
            # Adicione um print para verificar se o caminho está correto
            print(f"Procurando en.json em: {os.path.join(translations_dir, 'en.json')}")
            
            with open(os.path.join(translations_dir, "en.json"), "r") as f:
                translations = json.load(f)
            if key in translations:
                return translations[key]  # Retorna a tradução em inglês
        except Exception as e:
            log(f"{RED}Erro ao ler o arquivo de tradução para inglês: {e}{NC}")
        return key # Retorna a chave se o inglês também não for encontrado
    else:
        return None  # Retorna None se a tradução não for encontrada e fallback_to_key for False