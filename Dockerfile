# Usamos a versão do Python definida no seu runtime.txt (3.12)
FROM python:3.12-slim

# Evita arquivos .pyc e permite ver os logs no terminal mais rápido
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define a pasta principal lá dentro do container
WORKDIR /app

# Instala as dependências do Linux que o MySQL precisa
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia todo o código do projeto
COPY . /app/

# Expõe a porta 8000
EXPOSE 8000

# Comando padrão para rodar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
