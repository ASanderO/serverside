#!/bin/bash

# Construir a imagem do Docker
docker build -t apiflask .

# Iniciar o container a partir da imagem
docker run -d -p 5000:5000 --name serverside apiflask

# Executar o comando de inicialização do Flask no container
docker exec -it serverside flask db init
docker exec -it serverside flask db migrate
docker exec -it serverside flask db upgrade
