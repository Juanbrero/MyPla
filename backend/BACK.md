## Alembic (si se usa desde afuera, es decir, no se ejecuta desde el contenedor)
Para que se pueda utilizar el Alembic, y genere el codigo de migración, se debe utilizar con variables de entorno, ya que como se toma la URL de la BD desde database.py, y la url usa como ip **postgres** la cual no puede resolver el alembic, yo utilizo las varibles de entorno para que cuando para que cuando no esta el back encuentre None, y use la direccion de localhost.

- [Implementado](#implementado)
- [Falta](#falta)
- [Archivos](#armado-de-archivos-y-ejecución)
- [Alembic](#ejecutar-alembic)


# Metodo usado
Yo realice parte de la interaccóon desde fuera del contenedor, por lo que algunas de las instrucciones y cambios se basan en eso. Los cambios que hice son:
- database.py parametrizar URL, ya que no interactuaba desde el Docker
- if en env.py, como esto se realiza ahora desde el contenedor podria dejarse la instruccion **config.set_main_option("sqlalchemy.url", DATABASE_URL)**

A partir de levantar como esta hoy en dia, la interaccion debe hacerse desde el contenedor **backend**, esta configurado para que cuando inicie, como espera al postgres, cargue los archivos y arme las tablas, si se modifican seguir las instrucciones de [Alembic](#ejecutar-alembic) 

# YO
por lo que en database.py
se debe utilizar la linea 
~~~
DATABASE_URL = f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@postgres:5432/{getenv('POSTGRES_DB')}"
~~~
asi no genera problemas, se puede hacer pero habria que comentar y descomentar la url en el env.py

# RECORDAR
Descomentar en main el **@app.middleware("http")**, ya que esto permite usar el /docs y /redoc

# Preparacion (Recordatorios de lo que se hizo)
crear el alembic
~~~
cd backend
~~~
## Desde afuera de Docker
intalar dentro de un entorno virtual
~~~
pip install alembic
~~~
Inicar el Alembic
~~~
alembic init alembic
~~~

Se tiene que agregar la libreria **alembic** a **backend/requirements.txt** 


## Modificar archivos
alembic/env.py
agregar 
~~~
#Version con parametrizada
from app.models import *
from app.config.database import Base, DATABASE_URL

target_metadata = Base.metadata
#Se comprueba si dentro del DATABASE_URL esta el None
#como esta parametrizada y no esta levantado el back es True
#pero necesita estar el postgres
if 'None' in DATABASE_URL:
    config.set_main_option("sqlalchemy.url", 'postgresql://myuser:mypassword@localhost:5432/mydatabase')
else:
#esta linea funciona si levanta con el back
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
~~~
env.py
~~~
#version sin parametrizar, levanta con el back
from app.models import *
from app.config.database import Base, DATABASE_URL
target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", DATABASE_URL)
~~~

se debe agregar a alembic.ini
~~~
#Esta linea es ignorada porque se utiliza la info del env.py
sqlalchemy.url = postgresql://myuser:mypassword@localhost:5432/mydatabase
~~~


# Armado de archivos y ejecución
## Archivos

- models/MODELO.py
    -  crear modelo
- models/__init__.py
   - agregar import del modelo
   ~~~
    from .Profesional import Profesional
    #otros modelos
    from app.config.database import Base
   ~~~

### Para interacción
- app/bd/schemas/scheme_MODEL.py
   - esquema de respuestas
- app/bd/cruds/crud_MODEL.py
  -  Consultas

### API
- routes/ROUTE.py
   - endpoint que lo llamara

### Modificación para que levante las tablas cuando se levanta el backend
- docker-compose
  -  remplazar en backend command 
     - command: ["sh","-c","**alembic upgrade head** && uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload"]

### Ejecutar Alembic
- Docker
~~~
docker compose up -d --build --remove-orphans postgres backend 
docker exec -it backend bash
~~~
Para generar el archivo para la migracion se debe ejecutar, si no se coloca MENSAJE se usara el hash que genera alembic
~~~
$ alembic revision --autogenerate [-m "MENSAJE/COMENTARIO"]
~~~

Para ejecutarlo, esta linea toma los archivos de alembic/version, compara el hash almacendao en la BD y ejecuta para llegar hasta el ultimo
~~~
$ alembic upgrade head
~~~




## Relaciones 
~~~
#Relacion entre Objetos
#Si se utiliza como creador de columna Column no se utiliza esta funcion
from sqlalchemy.orm import relationship 

#Relacion en BD(Crea columnas en BD)
from sqlalchemy import ForeignKey, ForeignKeyConstrait 
~~~
### UNO A UNO
   - Usuario(usuario)
   ~~~
      id: Mapped[int] = mapped_column(primary_key=True)
      admin: relationship("Admin", back_populates="ususario")
   ~~~
   - Admin(admin)
   ~~~
      id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), primary_key=True)
   ~~~
### UNO A MUCHOS
- UNO:
   - MAPPED[list[MUCHOS]] = relationship
   ~~~
   Usuario.py
   id: Mapped[int] = mapped_column(primary_key=True)
   clases: Mapped[List["Clase"]] = relationship(back_populates="usuario")
   ~~~
- MUCHOS 
   - ForeignKey (si solo es un atributo FK de otra tabla)
      ~~~
      Clase.py
      user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id",on...))
      usuario: Mapped["Usuario"] = relationship(back_populates="clase")
      ~~~
   - ForeignKeyCostraint (si son mas de un atributo)
      ~~~
      __table_args__=(
         ForeignKeyCostraint(
            ["FK1", "FK2", ...],
            ["tabla.FK1, table.FK2, ....],
            on...)
      )
      ~~~


# Implementado
- Profesional
   - Crear un Profesional con ID autogenerado, por BD, y score en default 0 (llamado desde el back, no quedo en la BD) Revisar si la define cuando se recrea
   - Recuperar un Profesional por su ID
   - Recuperar todos lo Profesionales
   - Actualizar el score SOLO TEST
   - Eliminar un Profesional
- Topic
   - Crear un topico
   - Recuperar todos los topicos
   - Recuperar un topico (lo considero innecesario por si mismo)
- ProfesionalTopic
   - Agregar un topico a un profesional
   - Recuperar los topicos de un profesional por su ID
- Schedule (Agenda)
   - Controles que se realizan (CON)
      1. Valida que el tiempo de inicio y fin no sea el mismo y que inicio no sea menor a fin, en formato 24Hs ( inicio >= fin )
      2. Verifica que el horario no este incluido en los horarios almacenados ( hora in [inicio, inicio + 1H, inicio + 2H, .., fin] )
         - **Modificar para que considere la 30, ya que si se tiene 8:00-10:00 y se intenta ingresara 8:30-11:30 esta verificación admitiria ese horario**
      3. Solo almacena la hora y minutos (10:30:40) -> 10:30
      4. Control de que solo admita 00 o 30
   - Recurrent (CON 1, 2, 3, 4)
      1. Control de nombre de dia en español, **FALTA que sea todo en mayuscula o minuscula para evitar problemas**, por BD, Falta hacerlo en el back
      - Crear un evento recurrente, recibe un dia de la semana (Texto), un horario de inicio y fin, y un ID
      - Recuperar todos los evento recurrentes de un Profesional
      - Recuperar todos los eventos de un dia de un profesional
   - Specific (CON 1, 2, 3, 4)
      - Crear un dia especifico (date) para un profesional
      - recuperar los TODOS los dias especificos de todos los profesionales
      - Recuperar los dias de un profesional especifico
      - Conocer el estado de un dia especifico de un profesional, cancelado o no
      - Cancelar un dia especifico de un profesional

# Falta
- Delete de datos
- Que los datos **str** esten en mayuscula o miniscula
- Tablas faltantes (DER)
- Hacer que ID Profesional sea clave Foranea a User
- Agregar a las tablas cuando se creador, **Modificar para que lo haga**
- Superposiciones, entre specific y recurret
- Ver relacion con topicos
- TZ y ver si usamos AM y PM
- Testear si con la nueva definicion de Profesional, se tomo el default 0 en score (NO lo hace)
- Error que admite la duplicacion de horas al estar fuera de el rango, 8-10 e ingreas 6-11, permite ingresarlo

## Planteo de ideas
Para cambiar horarios se debera hacer updates de start, end y fecha de creacion/modificacion
- Para ampliar un horario existente recuperar horarios, si horario ingresado es mayor al horario guardo
   - En BD 8-10
   - Ingresa 6-10
   
   Se debera actualiza la PK(start) con el valor ingresado
- Para reducir
 - 6-10
 - 7-9

En BD
 - 7-9
 - 10 - 13
 - 15 - 20
Ingresa
   - 6-13
      - Eliminar la fila 10-13 y actualizar el end a las 13