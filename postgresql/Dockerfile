# Usar la imagen oficial de PostgreSQL
FROM postgres:latest

# Configurar variables de entorno
ENV POSTGRES_USER=miusuario
ENV POSTGRES_PASSWORD=mipassword
ENV POSTGRES_DB=midb

# Copiar el archivo SQL de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de PostgreSQL
EXPOSE 5432