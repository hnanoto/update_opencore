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
    translations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations")
    lang = get_system_language()

    # Tenta carregar o idioma completo (ex: pt_BR.json)
    lang_file = os.path.join(translations_dir, f"{lang}.json")
    if os.path.isfile(lang_file):
        try:
            with open(lang_file, "r") as f:
                translations = json.load(f)
            if key in translations:
                return translations[key]
        except Exception as e:
            log(f"{RED}Erro ao ler o arquivo de tradução para {lang}: {e}{NC}")

    # Tenta carregar a primeira parte do idioma (ex: pt.json)
    lang_short = lang.split("_")[0]
    lang_short_file = os.path.join(translations_dir, f"{lang_short}.json")
    if os.path.isfile(lang_short_file):
        try:
            with open(lang_short_file, "r") as f:
                translations = json.load(f)
            if key in translations:
                return translations[key]
        except Exception as e:
            log(f"{RED}Erro ao ler o arquivo de tradução para {lang_short}: {e}{NC}")

    # Se não encontrar a tradução e fallback_to_key for True, tenta o inglês
    if fallback_to_key:
        try:
            with open(os.path.join(translations_dir, "en.json"), "r") as f:
                translations = json.load(f)
            if key in translations:
                return translations[key]  # Retorna a tradução em inglês
        except Exception as e:
            log(f"{RED}Erro ao ler o arquivo de tradução para inglês: {e}{NC}")
        return key # Retorna a chave se o inglês também não for encontrado
    else:
        return None  # Retorna None se a tradução não for encontrada e fallback_to_key for False