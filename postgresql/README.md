# Uso de los programas:
## Iniciar contendor (usando shell)
El script revisa si existe la imagen, en caso contrario la crea.
Luego revisa si ya hay un contenedor, en caso contrario lo crea.
Si hay contenedor, lo levanta.
```
    ./run_postgres.sh
```
## Abrir la terminal e interactuar con la base de datos directamente.
Esto habre el cliente psql en modo interactivo.
```
    docker exec -it <id_container> psql -U miusuario -d midb
```
### Listar las bases de datos:
```
    \l
```
### Conectar a una bd especifica:
```
    \c <nombre bd>
```
### Ver tablas existentes:
```
    \dt
```
### Salir de la consola psql:
```
    \q
```
## No olvides parar el contenedor!!
```
    docker ps
    docker stop <id_contenedor>
```