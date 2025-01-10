from datetime import datetime
import os

# Cores para feedback visual
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0;m"  # Sem cor

# Arquivo de log
LOGFILE = f"update_opencore_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

def log(message):
    """Registra a mensagem no arquivo de log e a imprime na tela."""
    with open(LOGFILE, "a") as logfile:
        logfile.write(message + "\n")
    print(message)