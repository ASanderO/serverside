# Use a imagem base do Python
FROM python:3.9-slim

# Configuração do ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Diretório de trabalho no container
WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instale as dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do aplicativo
COPY . /app/

# Exponha a porta do Flask
EXPOSE 5000

# Comando para rodar o servidor Flask
CMD ["flask", "run", "--host=0.0.0.0"]
