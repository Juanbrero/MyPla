# Usar la imagen oficial de PostgreSQL usando alpine como base
FROM postgres:17.4-alpine3.21

# Configurar variables de entorno (esto esta mal)
ENV POSTGRES_USER=miusuario
ENV POSTGRES_PASSWORD=mipassword
ENV POSTGRES_DB=midb

# Copiar el archivo SQL de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de PostgreSQL
EXPOSE 5432