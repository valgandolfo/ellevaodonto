#!/bin/bash

# Muda para o diretório de onde o script está sendo executado
cd "$(dirname "$0")"

echo "======================================"
echo "1 - Ativando o ambiente virtual..."
echo "======================================"
source venv/bin/activate

echo "======================================"
echo "2 - Instalando as dependências..."
echo "======================================"
pip install -r requirements.txt

echo "======================================"
echo "3 - Executando o servidor do Django..."
echo "======================================"
python manage.py runserver
