# Modulo PostgreSQL
## Tablas
### TABLA del Profesional (profesional):
| Nombre Attrib   | Tipo   | Comentario   |
|:---------------:|:------:|:------------:|
| user_id       | SERIAL | PK |

### Tabla del Evento (evento):

| Nombre Attrib   | Tipo   | Comentario   |
|:---------------:|:------:|:------------:|
| event_timestamp | TIMESTAMP NOT NULL | PK |
| user_id | INTEGER NOT NULL | PK/FK con tabla profesional |
| titulo | VARCHAR(255) NOT NULL | |
| descripcion | TEXT NOT NULL | |

## Triggers:
### BEFORE INSERT ON evento:
```
validar_ranura_horaria():EXCEPTION
```
* Valida si el nuevo evento se solapa con otro evento ya registrado (1 hora de diferencia).
* Si ese fuera el caso, tira un EXCEPTION

## Procedures (o FUNCTION):
### get_eventos_profesional:
```
    get_eventos_profesional(id_profesional_input INTEGER)
```
* Retorna 'TABLE' con todos los eventos asociados a la id del profesional.
Usage:
```
    SELECT * FROM get_eventos_profesional(1);
```
## Iniciar contendor (usando shell)
El script revisa si existe la imagen, en caso contrario la crea (modo daemon).
Luego revisa si ya hay un contenedor, en caso contrario lo crea (modo daemon).
Si hay contenedor, lo levanta (modo daemon).
```
    ./run_postgres.sh
```
## Ante dudas o errore consultar el log:
```
    docker logs postgres_container
```
## Abrir la terminal e interactuar con la base de datos directamente.
Esto habre el cliente psql en modo interactivo.
```
            docker exec -it postgres_container sh
(en sh)     psql -U miusuario -d midb
```
### Listar las bases de datos:
```
    \l
```
### Conectar a una bd especifica:
Por defecto esta conectado a la base de datos 'midb'
```
    \c <nombre bd>
```
### Ver tablas existentes:
```
    \dt
```
### Ver triggers existentes:
```
SELECT
    trigger_schema,
    trigger_name,
    event_object_table
FROM 
    information_schema.triggers
ORDER BY 
    event_object_table;
```
### Ver stored procedures (user created objects):
```
    \df
```
### Salir de la consola psql:
```
    \q
```
### Cargar manualmente el sql (si no lo hizo el Dockerfile)
```
    \i /docker-entrypoint-initdb.d/init.sql
```
## No olvides parar el contenedor!!
```
    docker ps
    docker stop <id_contenedor>
```

# Limitaciones
* Para aplicar cambios a la BD, hace falta eliminar el container (y tambien la imagen) y volver a ejecutar el script.
```
    docker stop postgres_container && docker rm postgres_container && docker rmi mi_postgres
```

# Glitches:
* Puede que a la primera vez que usar el script sh, al entrar a la terminal del contenedor no este conectada la bd. Cerralo y espera un par de segundos para abrirlo.