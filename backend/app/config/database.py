from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import importlib
from os import listdir

from os import getenv

# 📌 Configura la conexión a PostgreSQL

DATABASE_URL = getenv("DATABASE_URL")

# 📌 Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

# 📌 Crea una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📌 Base para los modelos
Base = declarative_base()

# 📌 Función para obtener la sesión en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import_all_module()
    Base.metadata.create_all(bind=engine)


#Function to read module directorie, and charge models of tables
def import_all_module():
    #import models to create BD
    for filename in listdir("/app/app/models"):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f'app.models.{filename[:-3]}'
            
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError as e:
                print(f"Failed to import module {module_name}: {e}")
                continue
