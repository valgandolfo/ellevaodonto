#!/bin/bash

# Volta para a pasta onde o script está
cd "$(dirname "$0")"

# Define o nome do arquivo de backup formatado com data e hora
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backup_elleva_$TIMESTAMP.tar.gz"

echo "======================================"
echo " Iniciando backup do projeto..."
echo "======================================"

# Executa a compactação do diretório raiz
# --exclude ignora a pasta venv e imagens como solicitado
tar -czf "$BACKUP_FILE" \
    --exclude="./venv" \
    --exclude="./imagens" \
    --exclude="./.git" \
    --exclude="*/__pycache__" \
    --exclude="*.pyc" \
    .

echo "Backup gerado com sucesso: $BACKUP_FILE"
echo "======================================"
