## Alembic
Para que se pueda utilizar el Alembic, y genere el codigo de migración, se debe utilizar con variables de entorno, ya que como se toma la URL de la BD desde database.py, y la url usa como ip **postgres** la cual no puede resolver el alembic, yo utilizo las varibles de entorno para que cuando para que cuando no esta el back encuentre None, y use la direccion de localhost.

por lo que en database.py
se debe utilizar la linea 
~~~
DATABASE_URL = f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@postgres:5432/{getenv('POSTGRES_DB')}"
~~~
asi no genera problemas, se puede hacer pero habria que comentar y descomentar la url en el env.py

crear el alembic
~~~
cd backend
~~~
intalar dentro de un entorno virtual
~~~
pip install alembic
~~~
Inicar el Alembic
~~~
alembic init alembic
~~~

Se tiene que agragar la libreria **alembic** a **backend/requirements.txt** 

modificar archivos
alembic/env.py
agregar
~~~
from app.models import *
from app.config.database import Base, DATABASE_URL

target_metadata = Base.metadata
#Se comprueba si dentro del DATABASE_URL esta el None
#como no esta levantado el back es True
#pero necesita estar el postgres
if 'None' in DATABASE_URL:
    config.set_main_option("sqlalchemy.url", 'postgresql://myuser:mypassword@localhost:5432/mydatabase')
else:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

~~~

se debe agregar a alembic.ini
~~~
#Esta linea es ignorada porque se utiliza la info del env.py
sqlalchemy.url = postgresql://myuser:mypassword@localhost:5432/mydatabase
~~~

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
- app/bd/schemas/scheme_MODEL.py
   - esquema de respuestas
- app/bd/cruds/crud_MODEL.py
  -  Consultas
- routes/ROUTE.py
   - endpoint que lo llamara
- docker-compose
  -  remplazar en backend command 
     - command: ["sh","-c","alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload"]


Levantamos el postgres
~~~
docker compose up -d postgres
~~~
Para generar el archivo para la migracion se debe ejecutar dentro del directorio backend
~~~
alembic revision --autogenerate [-m "MENSAJE/COMENTARIO"]
~~~



Luego ejecutar el docker compose
~~~
docker compose up --build --remove-orphans backend
~~~
