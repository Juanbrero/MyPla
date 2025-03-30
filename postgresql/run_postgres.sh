#!/bin/bash

CONTAINER_NAME="postgres_container"
IMAGE_NAME="mi_postgres"
POSTGRES_USER="miusuario"
POSTGRES_PASSWORD="mipassword"
POSTGRES_DB="midb"

# Verifica si el contenedor ya existe
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "El contenedor $CONTAINER_NAME ya existe."

    # Si el contenedor existe pero está detenido, lo iniciamos
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo "El contenedor ya está en ejecución."
    else
        echo "Iniciando el contenedor detenido..."
        docker start $CONTAINER_NAME
    fi
else
    echo "Creando y ejecutando un nuevo contenedor de PostgreSQL en modo daemon..."
    
    # Construir la imagen (si no está construida previamente)
    if [ -z "$(docker images -q $IMAGE_NAME)" ]; then
        echo "Imagen $IMAGE_NAME no encontrada. Construyéndola..."
        docker build -t $IMAGE_NAME .
    fi

    # Ejecutar el contenedor en modo daemon (-d) con las variables de entorno correctas
    docker run -d --name $CONTAINER_NAME \
        -e POSTGRES_USER=$POSTGRES_USER \
        -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
        -e POSTGRES_DB=$POSTGRES_DB \
        -p 5432:5432 $IMAGE_NAME

    echo "Contenedor $CONTAINER_NAME iniciado en modo daemon."
fi
