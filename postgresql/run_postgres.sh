#!/bin/bash

CONTAINER_NAME="postgres_container"

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
    echo "Creando y ejecutando un nuevo contenedor de PostgreSQL..."
    
    # Construir la imagen (si no está construida previamente)
    docker build -t mi_postgres .

    # Ejecutar el contenedor si no existe
    docker run --name $CONTAINER_NAME -p 5432:5432 -d mi_postgres
fi
