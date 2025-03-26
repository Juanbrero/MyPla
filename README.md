# MyPla

## Indice
* [Integrantes del equipo](#integrantes-del-equipo)
* [Postgress](#iniciar-postgres-con-tablas)


## Integrantes del equipo

| Alumno | Github |
| ----   | ---- |
| Juan Manuel Brero | [JuanBrero](https://github.com/JuanBrero) |
| Matias Herrneder | [MatiasHerrneder](https://github.com/MatiasHerrneder) |   
| Federico Claros Garcia | [federicoclarosv15](https://github.com/federicoclarosv15) |
| Thiago Puyelli| [ThiagoPuyelli](https://github.com/ThiagoPuyelli) |
| Esteban Viani | [eviani](https://github.com/eviani) |  

~~~
docker-compose up -d para levantar contenedor
docker ps para verificar que el contenedor esta  corriendo
docker exec -it postgres_db psql -U myuser -d mydatabase
~~~

## Iniciar Postgres con tablas

Para que el postgres inicie con las tablas, hay dos opciones
* si ya fue ejecutado el compose, se debera eliminar el volumen, esto eliminara **toda** la información de la **BD**
    ~~~
    docker volumes rm mypla_postgress_data
    docker compose up -d
    ~~~
* ejecutar el SQL de /SQL/base.sql

Se crearan tres tablas independients __eventos__, __users__ y __teacher__ (Vacia)
- Eventos:
    - id PK 
    - titulo NOT NULL
    - descripcion
    - fecha NOT NULL
    - creadro_en 
- Users:
    - id PK
    - name NOT NULL
- Teacher (Vacia):
    - id PK
    - name NOT NULL
* Consulta
    * accediendo a [localhost/event](http://localhost:8002/event), podra ver la consulta a la tabla evento.
* Insersiones, con respuesta de consulta
    * accediendo a [localhost/add-user1](http://localhost:8002/add-user1), se utiliza el metodo de asignación para insertar un usuario llamado **PEPE**
    * accediendo a [localhost/add-user2](http://localhost:8002/add-user2), se utiliza el metodo de diccionario para insertar un usuario llamado **Luis**
    * accediendo a [localhost/add-users](http://localhost:8002/add-users), se  insertan dos usuarios **USER1** y **USER2**, usando un diccionario.
