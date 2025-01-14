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

# Variável global para armazenar as traduções em memória
TRANSLATIONS = {}

def load_translations():
    """Carrega as traduções de todos os arquivos JSON para o dicionário TRANSLATIONS."""
    global TRANSLATIONS
    translations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations")
    
    for filename in os.listdir(translations_dir):
        if filename.endswith(".json"):
            lang = filename[:-5]  # Remove a extensão .json
            filepath = os.path.join(translations_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f: # Adicionado encoding="utf-8"
                    TRANSLATIONS[lang] = json.load(f)
            except Exception as e:
                log(f"{RED}Erro ao carregar traduções para {lang}: {e}{NC}")

def get_system_language():
    """Detecta o idioma preferido do usuário usando a biblioteca locale."""
    try:
        lang, encoding = locale.getlocale()
        if lang:
            return lang
        else:
            # Tenta obter o idioma usando variáveis de ambiente
            lang = os.environ.get('LANG') or os.environ.get('LC_ALL')
            if lang:
                return lang.split('.')[0]  # Retorna apenas a parte do idioma (ex: en_US -> en)
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
    """Retorna a tradução para a chave especificada no idioma do sistema."""
    lang = get_system_language()

    # Tenta encontrar a tradução para o idioma completo
    if lang in TRANSLATIONS:
        if key in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][key]

    # Tenta encontrar a tradução para a primeira parte do idioma
    lang_short = lang.split("_")[0]
    if lang_short in TRANSLATIONS:
        if key in TRANSLATIONS[lang_short]:
            return TRANSLATIONS[lang_short][key]

    # Se não encontrou a tradução, tenta carregar do en.json se fallback for True
    if fallback_to_key:
        if "en" in TRANSLATIONS:
            if key in TRANSLATIONS["en"]:
                return TRANSLATIONS["en"][key]
        else:
            log(f"{RED}Erro: Arquivo de tradução para inglês (en.json) não encontrado!{NC}")
        return key  # Retorna a chave se não encontrar em inglês e fallback_to_key for True
    else:
        return None  # Retorna None se a tradução não for encontrada e fallback_to_key for False

# Carrega as traduções no início do script
load_translations()
