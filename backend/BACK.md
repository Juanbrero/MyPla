# Backend

   | LINK | Descripcion|
   | --- | ---| 
   | [Ejecutar main](#ejecutar-mainpy-desde-afuera) | Cambios para que se pueda utilizar Alembic sin ingresar a Docker |
   | [RECORDAR](#recordar) | Importante Cambios que se deben hacer para salir a producción |
   | [Preparación OMITIR](#preparacion-recordatorios-de-lo-que-se-hizo) | Metodo utilizado para crear los archivos iniciales, usar si se empieza desde 0|
   | [Archivos](#armado-de-archivos-y-ejecución) | Archivos que deben crearse y modificarse |
   | [Alembic](#ejecutar-alembic) | Ejecución de Alembic, comandos a ejecutar si se utiliza con Docker o con venv | 
   | [Implementado](#implementado) | Tablas y funciones implementadas |
   | [Falta](#falta) | Funciones, controles y trabajos que faltan implementar |
   | [Test](#test) | Test |
---
## [JSON](#json)

| Link |  |
| ---   |---|
| [Query](#query)|  |
|  |[Users](#query-users)|
|  |[Professional](#query-professional)|
|  |[Topics](#query-topics)|
|  |[Professional Topic](#query-professional-topic)|
|  |[Recurrent](#query-recurrent)|
|  |[Specific](#query-specific)|
|  |[Exception](#query-exception)|
|[Response](#response)|  |
|  |[Users](#response-users)|
|  |[Professional](#response-professional)|
|  |[Topics](#response-topics)|
|  |[Professional Topic](#response-professional-topic)|
|  |[Recurrent](#response-recurrent)|
|  |[Specific](#response-specific)|
|  |[Exception](#response-exception)|
||[Response Front](#response-to-front)|

---
# Icecream
Modulo para evitar usar print( ) y olvidar donde estan.
Con este modulo podremos colocar salidas, y dar un poco de contexto, sabiendo donde paso y con la posibilidad de desactivarlo para no tener que buscar todos las ocurrencias.

Se puede importar de dos maneras: 
- importarlo individualmente en cada modulo
~~~
from icecream import ic
~~~
- O hacer un import e instalación en el modulo padre "main", lo que lo deja disponible en todos lo modulos sin necesidad de importar en cada uno
~~~
from icecream import install
install()
#esto no permitira conocer en que archivo esta el ic
# contextAbsPath=True => path absoluto del archivo 
## ic| /home/esteban/SIP/MyPla/backend/app/routes/topic.py:24 in get_topic()
##    f'GET TOPIC': 'GET TOPIC'
ic.configureOutput(contextAbsPath=False, includeContext=True)
~~~
sabremos en que modulo ocurre cada evento
~~~
ic| topic.py:24 in get_topic()- f'GET TOPIC': 'GET TOPIC'
~~~
Para ejecutarlo se llama
~~~
ic(VAR) # VAR => puede ser una variable, un f-string, funciones, etc. 
ic(os.env('RELOAD'))
ic('TOPIC')
ic(f'Valor B {Bvalues}')
~~~

Desactivar, esto lo desactiva para todos los modulos, por lo que es recomendable habilitar y deshabilitar desde Main
~~~
ic.disable()
~~~
---


# Ejecutar main.py Desde afuera
Levantamos la BD
~~~
$ docker compose up -d --build --remove-orphans postgres
~~~
Agregamos el host **postgres** a los hosts conocidos, para que pueda encontrarlo desde fuera
~~~
sudo nano /etc/hosts
127.0.0.1 postgres
~~~
Ahora podremos interactuar con la BD, desde fuera de Docker

En /backend y en el **entorno virtual**
~~~
$ cd ~/backend
# usar el metodo de activacion, de venvs, que uses regularmente
$ source ./vevn/bin/activate
venv$ pip install -r requirements.txt
venv$ python -m app.main
~~~


# RECORDAR
PARA PRODUCCION, quitar el if, que admite el /docs

# Preparación (Recordatorios de lo que se hizo)
Ya implementado, es a manera de memorias de como se hizo el proceso, [continuar](#armado-de-archivos-y-ejecución)
crear el alembic
~~~
cd MyPla/backend
~~~
## Desde afuera de Docker
instalar dentro de un entorno virtual
~~~
pip install alembic
~~~
Crear el Alembic
~~~
alembic init alembic
~~~
Esto genera backend/alembic.ini, /backend/alembic/

## Modificar archivos
alembic/env.py

Agregar 
~~~
# importa los modelos de app/models
# si no esta el archivo __init__.py, importa todos
# si esta solo los que importados en ese archivo
from app.models import *

from app.config.database import Base, DATABASE_URL
target_metadata = Base.metadata
# Esta linea toma la definición de la URL de config/database.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)
~~~

se debe agregar a alembic.ini, esta linea es sobre escrita por la definición en env.py, pero si 
~~~
sqlalchemy.url = postgresql://myuser:mypassword@localhost:5432/mydatabase
~~~

### Modificación para que levante las tablas cuando se inicia el backend desde Docker Compose
- docker-compose
  -  remplazar en backend command 
     - command: ["sh","-c","**alembic upgrade head** && uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload"]

# Fin preparación

# Armado de archivos y ejecución
## Archivos

- models/MODELO.py
    -  crear modelo de la tabla
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
  -  Consultas validas

### API
- routes/ROUTE.py
   - endpoint que lo llamara


### Ejecutar Alembic
- Siempre con Postgres corriendo
   - Con Docker
   ~~~
   docker compose up -d --build --remove-orphans postgres backend 
   docker exec -it backend bash
   ~~~

   - Con venv
   ~~~
   venv$ cd backend
   ~~~

Para generar el archivo para la migración se debe ejecutar 
~~~
$ alembic revision --autogenerate [-m "MENSAJE/COMENTARIO"]
~~~
Si no se coloca MENSAJE, util para orientar que acción realizara el codigo, se usara el hash que genera alembic. RECOMENDACIÓN: Revisar el archivo autogenerado para confirmar que se creo lo esperado.

Para ejecutarlo, esta linea toma los archivos de alembic/version, compara el hash almacendao en la BD y ejecuta para llegar hasta el ultimo
~~~
$ alembic upgrade head
~~~
> [! Note]
> El ciclo de trabajo es generar el archivo de migración y ejecutar el upgrade, es decir, se debe ejecutar 
> ~~~
> alembic revision ..
> alembic upgrade ..
> ~~~
> Antes de poder generar un nuevo archivo de migración



# Armado de modelos
## Relaciones (https://chatgpt.com/share/680bed6f-c854-8009-8ca7-22d350f08eb2)
~~~
#Relacion entre Objetos
from sqlalchemy.orm import relationship 

#Relacion en BD(Crea columnas en BD)
from sqlalchemy import ForeignKey, ForeignKeyConstrait 
~~~
- ForeignKey (si solo es un atributo FK de otra tabla)
~~~
 atr : Maped[TYPE] = mapped_column(ForeignKey('__table__name', ...), ...) 
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
### UNO A UNO
   - User (users)
   ~~~
      user_id: Mapped[int] = mapped_column(primary_key=True)
      professional: Mapped['Professional'] relationship(back_populates="user", cascade='all, delete-orphan')
   ~~~
   - Professional (profesional)
   ~~~
      prof_id: Mapped[int] = mapped_column(ForeignKey("users.user_id",ondelete='CASCADE'), primary_key=True)
      user: Maped['User'] = relationship(back_populates='professional')
   ~~~
### UNO A MUCHOS
- UNO:
   - MAPPED[List[MUCHOS]] = relationship
   - Professional (profesional)
   ~~~
   from typing import List

   prof_id: Mapped[int] = mapped_column(ForeignKey("usuer.user_id",ondelete='CASCADE'), primary_key=True)
   user: Maped['User'] = relationship(back_populates='professional')

   recurrent: Mapped[List["RecurrentSchedule"]] = relationship(back_populates="professional", cascade="all, delete-orphan")
   ~~~

- MUCHOS 
   
   - RecurrentSchedule (recurrentschedule) Un solo atributo

         ~~~
         week_day: Mapped[int] = mapped_column(primary_key= True)
         prof_id: Mapped[str] = mapped_column(ForeignKey("professional.prof_id", ondelete="CASCADE"), primary_key= True)

         professional: Mapped["Professional"] = relationship(back_populates= "recurrent")
         ~~~ 

      - TopicSpecific (topicspecific) Varios atributos
      ~~~
      prof_id: Mapped[str] = mapped_column(primary_key=True) #FK -> ProfessinalTopic
      topic_name: Mapped[str] = mapped_column(primary_key=True) #FK -> ProfessionalTopic
      topic: Mapped['ProfessionalTopic'] = relationship(back_populates='specific_topic')

      __table_args__= (
        ForeignKeyConstraint(
        ['prof_id', 'topic_name'], 
        ['professionaltopic.prof_id', 'professionaltopic.topic_name'],
        ondelete='CASCADE',
        onupdate='CASCADE'
      ),
      )
      ~~~


# Implementado
- Usuario
   - Crear un usuario (id, name) donde name=id
   - eliminar un usuario
- Profesional
   - Crear un Profesional con score en default 0
   - Recuperar un Profesional por su ID
   - Recuperar todos lo Profesionales
   - Actualizar el score SOLO TEST
   - Eliminar un Profesional
- Topic
   - Crear un topico
   - Recuperar todos los topicos
- ProfesionalTopic
   - Agregar un topico a un profesional
   - Recuperar los topicos de un profesional por su ID
   - Eliminar un topico de un profesional
- Schedule (Agenda)
   - Controles que se realizan (CON)
      1. Valida que el tiempo de inicio y fin no sea el mismo y que inicio no sea menor a fin, en formato 24Hs ( inicio >= fin )
      2. Verifica que el horario no este incluido en los horarios almacenados ( hora in [inicio, inicio + 1H, inicio + 2H, .., fin] )
         - **Modificar para que considere la 30, ya que si se tiene 8:00-10:00 y se intenta ingresara 8:30-11:30 esta verificación admitiria ese horario**
      3. Solo almacena la hora y minutos (10:30:40) -> 10:30
      4. Control de que solo admita 00 o 30
   - Recurrent (CON 1, 2, 3, 4)
      - **El calendario lo crea TopicRecurrent, el recibe la peticion y realiza las inserciones**
      1. Control por DB y Back que el valor este entre 1-7
      - Crear un evento recurrente, recibe un dia de la semana (int), un horario de inicio y fin, un  prof_ID y una lista de topicos. Ver esquema [Query](#query-recurrent)
      - Recuperar todos los evento recurrentes de un Profesional
   - Specific (CON 1, 2, 3, 4)
      - Crear un dia especifico (date) para un profesional en base a [Query](#query-specific)
      - recuperar los TODOS los dias especificos de todos los profesionales
   - Excepciones (CON 1, 2, 3, 4) (isCanceling= True)
      - Crea un dia especifico no disponible [Query](#query-exception)
      - Recupera TODOS los dias excepcionales

# Prioridad
   1. Recurrente
   2. Especifico 
   3. Excepción
   4. Clases
   5. Evento


# Falta
- Definir como sera la interaccion con Profesional y Alumno, como y que se pide y devuelve
- Agregar peticion de dia especifico por mes
- Bloquear exceptions si no hay un recurrente asociado
- Armado de excepciones, leer excepciones -> day.isweekend() -> recurrent.week_day - day-hours
   - Horario 8-16 -> Lunes
   - Proximo lunes 2025-04-21 dara 10-18
      - Especifico:
         - 2025-04-21
         - S 10
         - E 18
         - iscanceling: False
      - Exception:
         - 2025-04-21
         - S 8
         - E 16
         - Iscanceling: True



- Delete de datos 
- Tablas faltantes (DER)
- Agregar a las tablas cuando se creador, **Modificar para que lo haga** Cuales
- TZ y ver si usamos AM y PM ??
- Error que admite la duplicacion de horas al estar fuera de el rango, 8-10 e ingreas 6-11, permite ingresarlo
- Ver como le agregamos atributo a topic como propuesto o algo asi, para que se almacene el topico y se deba aprobar
- Considerar las 30, para definir incluido
   - En BD 8-12 e ingresa 8:30-12:30 se admite esa inserción


## Planteo de como se debera hacer acualizacion (EN PROCESO de plantear)
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


# JSON

## Query
### Query Users 
 - Create 
 POST /create/{user_id}
 - Get  
 GET /get/all
 - Delete 
 DELETE /delete/{user_id}
---
### Query Professional
 - Create solo para pruebas, se realiza por back directamente 
  POST /professional/{prof_id}/create
 - Get one
 GET /professional/{prof_id}
 - Get all
 GET /professional/{prof_id}
 - Update (score) Se realizaria por back
 PUT /professional/{prof_id}/score
 ~~~
 {
  "score": 0
   }
 ~~~
 - Delete 
 DELETE /professional/{prof_id}
---
### Query Topics
 - Create (Se convierte en mayuscula el string al almacenarlo)
 POST /topics/create
 ~~~
 {
  "topic_name": "string"
   }
 ~~~
 - Get all
 GET /topics/get
---
### Query Professional Topic
- Create
POST /topics/prof/{prof_id}/add
~~~
{
  "topic_name": "string",
  "price_class": 0
}
~~~
- Get
GET /topics/prof/{prof_id}
- Delete
DELETE /topics/prof/{prof_id}
~~~
{
  "topic_name": "string"
}
~~~
---
### Query Recurrent
   - Create: formato de hora 24Hs 
   POST /prof/{prof_id}/agenda/create/recurrent
   ~~~
   { "week_day": 2,
        "start": "00:30",
        "end": "02:30",
        "topics": [
            {
            "topic_name": "ingles"
            },
            {
            "topic_name": "frances"
            }
            ]
        }
   ~~~
   - Get
   GET /prof/{prof_id}/agenda/get/recurrent
---
### Query Specific
   - Create dia particular (isCanceling= False)
   POST /prof/{prof_id}/agenda/create/spec
   ~~~
   {
            "day": "2025-04-30",
            "start": "20:30:25.443Z",
            "end": "22:30:25.443Z",
            "topics": [
                {
                "topic_name": "fisica"
                }
            ]
        }
   ~~~
   - Get dias especificos
   GET /prof/{prof_id}/agenda/get/recurrent

### Query Exception
   - Create
      POST /prof/{prof_id}/agenda/create/exception
      ~~~
      {
      "start": "21:38:04.836Z",
      "end": "21:38:04.836Z",
      "day": "2025-05-01"
      }
      ~~~
   - Get
      GET /prof/{prof_id}/agenda/get/exception

## Response
mes -> 
   select * from recurrent where mes == mes 
      join topicosRecurrent.week, start => lista(TOPICOS)
   select * from specific where day.moth == mes
      -> if iscanceling => exception
      -> select topic from topic => lista(TOPICOS)

### Response Users
 - Create 
 POST /create/{user_id}
 ~~~
 {'user_id': ,
  'name': }
  {'error': }
 ~~~
 - Get  
 GET /get/all
 ~~~
 [
   {'user_id': ,
  'name': }
  ]
 ~~~
 - Delete 
 DELETE /delete/{user_id}
 ~~~
 {'OK': 'OK'}
 {'error': }
 ~~~
---
### Response Professional
 - Create solo para pruebas, se realiza por back directamente 
  POST /professional/{prof_id}/create
  ~~~
  {'info': }
  {'error': }
  ~~~

 - Get one
 GET /professional/{prof_id}
 ~~~
 {'prof_id': , 
 'score': }
 {'error': }
 ~~~
 - Get all
 GET /professional/{prof_id}
 ~~~
 [
   {'prof_id': , 
 'score': },
 {'prof_id': , 
 'score': }
 ]
 ~~~
 - Update (score) Se realizaria por back
 PUT /professional/{prof_id}/score
 ~~~
 {
  "prof_id": "string",
  "score": 0
}
 ~~~
 - Delete 
 DELETE /professional/{prof_id}
 ~~~
 {'info': }
 {'error': }
 ~~~
---
### Response Topics
 - Create
 POST /topics/create
 ~~~
 {
  "topic_name": "string"
   }
 ~~~
 - Get all
 GET /topics/get
 ~~~
 [
    {
  "topic_name": "string"
   },
    {
  "topic_name": "string"
   }
   ]
 ~~~
---
### Response Professional Topic
- Create
POST /topics/prof/{prof_id}/add
~~~
{
  "prof_id": ,
  "topic_name": "string",
  "price_class": 0
}
~~~
- Get
GET /topics/prof/{prof_id}
~~~
[
   {
  "prof_id": ,
  "topic_name": "string",
  "price_class": 0
},
{
  "prof_id": ,
  "topic_name": "string",
  "price_class": 0
}
]
~~~
- Delete
DELETE /topics/prof/{prof_id}
~~~
{
  "prof_id": ,
  "topic_name": "string"
}
~~~
---
### Response Recurrent
   - Create: formato de hora 24Hs 
   POST /prof/{prof_id}/agenda/create/recurrent
   ~~~
   { "week_day": 2,
        "start": "00:30",
        "end": "02:30",
        "topics": [
            {
            "topic_name": "ingles"
            },
            {
            "topic_name": "frances"
            }
            ],
         "prof_id": 
        }
   ~~~
   - Get
   GET /prof/{prof_id}/agenda/get/recurrent
   ~~~
   {
  "recurrent": [
    {
      "week_day": 0,
      "start": "17:19:12.001Z",
      "end": "17:19:12.001Z",
      "topics": [
        {
          "topic_name": "string"
        }
      ]
    }
  ]
   }
   ~~~
---   
### Response Specific
   - Create dia particular (isCanceling= False)
   POST /prof/{prof_id}/agenda/create/spec
   ~~~
   {
  "day": "2025-05-01",
  "start": "17:21:24.170Z",
  "end": "17:21:24.170Z",
  "topics": [
    {
      "topic_name": "string"
    }
  ],
  "prof_id": "string",
  "isCanceling": false
   }
   ~~~
   - Get dias especificos
   GET /prof/{prof_id}/agenda/get/recurrent
   ~~~
   {
  "specific": [
    {
      "day": "2025-05-01",
      "start": "17:22:00.459Z",
      "end": "17:22:00.459Z",
      "topics": [
        {
          "topic_name": "string"
        }
      ]
    }
   ]}
   ~~~

### Response Exception
   - Create
      POST /prof/{prof_id}/agenda/create/exception
      ~~~
      {
         "start": "21:40:07.116Z",
         "end": "21:40:07.116Z",
         "day": "2025-05-01"
      }
      ~~~
   - Get
      GET /prof/{prof_id}/agenda/get/exception
      ~~~
      {
         "exception": [
            {
                  "start": "21:40:57.854Z",
                  "end": "21:40:57.854Z",
                  "day": "2025-05-01"
               }
         ]
    }
      ~~~


### Response to Front
- Mostrar horario:
   - Profesional
   ~~~
      {recurret: [{
         start:time,
         end: time,
         week_day: integer o enum (1-7),
         topics: string[]
      }],
       specific:[{
         day: date,
         start: time,
         end: time,
         topics: string[]
       }],
       exception:[{
         day: date,
         start: time,
         end: time         
       }],
       class:[{
         day: date,
         start: time,
         topic: string
       }],
       event:[{
         day: date,
         start: time,
         end: time,
         id_event: string
       }]
      }
   ~~~
   - Alumno
   ~~~
      {recurret: [{
         start:time,
         end: time,
         week_day: integer o enum (1-7),
         topics: string[]
      }],
       specific:[{
         day: date,
         start: time,
         end: time,
         topics: string[]
       }],
       exception:[{
         day: date,
         start: time,
         end: time         
       }],
       event:[{
         day: date,
         start: time,
         end: time,
         id_event: string
       }]
      }   
   ~~~
 

# Test
En backend/test/, se encuentra el archivo test_EP_bd.py, donde se realizan inserciones para que la BD tenga datos.

Luego de la ejecución las tablas quedaran asi:


-  users
   - user_id: a
      - name: a
   - user_id: b
      - name: b 
   - user_id: z
      - name: z

- professional
 - prof_id: a
   - score: 0
 - prof_id: b
   - score: 0
 - prof_id: z
   - score: 0

- topic
   - topic_name: INGLES
   - topic_name: FRANCES
   - topic_name: FISICA
   - topic_name: FILOSOFIA

- professionaltopic
   - topic_name: INGLES
      - prof_id: a
      - price_class: 1
   - topic_name: FRANCES
      - prof_id: a
      - price_class: 1
   - topic_name: FILOSOFIA
      - prof_id: z
      - price_class: 1
   - topic_name: INGLES
      - prof_id: z
      - price_class: 2
   - topic_name: FISICA 
      - prof_id: b
      - price_class: 3

- recurrentschedule
   - week_day: 2
      - start: 00:30
      - prof_id: a
      - end: 02:30
   - week_day: 1
      - start: 00:30
      - prof_id: a
      - end: 02:30
   - week_day: 1
      - start: 17:30
      - prof_id: z
      - end: 18:30
   - week_day: 1
      - start: 15:30
      - prof_id: z
      - end: 23:30

- topicrecurrent
   - prof_id: a
      - topic_name: INGLES 
      - start: 00:30
      - week_day: 2
   - prof_id: a
      - topic_name: FRANCES
      - start: 00:30
      - week_day: 2
   - prof_id: a
      - topic_name: INGLES 
      - start: 00:30
      - week_day: 1
   - prof_id: a
      - topic_name: FRANCES 
      - start: 00:30
      - week_day: 1
   - prof_id: z
      - topic_name: FILOSOFIA 
      - start: 17:30
      - week_day: 1
   - prof_id: z
      - topic_name: FILOSOFIA 
      - start: 15:30
      - week_day: 2
   - prof_id: z
      - topic_name: INGLES 
      - start: 15:30
      - week_day: 2

- specificschedule
   - day: 2025-04-30
      - start: 20:30
      - prof_id: b
      - end: 22:30
      - isCanceling: False 
   - day: 2025-05-01
      - start: 18:30
      - prof_id: a
      - end: 19:30
      - isCanceling: True

- topicspecific
   - prof_id: b
      - topic_name: FISICA
      - start: 20:30
      - day: 2025-04-30   
   
   
      
