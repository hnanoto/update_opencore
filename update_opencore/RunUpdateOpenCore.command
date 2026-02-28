#!/bin/bash

# Caminho absoluto do script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ativa o ambiente virtual se existir
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Criando ambiente virtual Python..."
    python3 -m venv "$SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Instala dependências
echo "Instalando dependências necessárias..."
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"

# Executa o script principal
python3 "$SCRIPT_DIR/main.py"

