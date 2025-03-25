from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 📌 Configura la conexión a PostgreSQL
DATABASE_URL = "postgresql://myuser:mypassword@postgres:5432/mydatabase"

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
    Base.metadata.create_all(bind=engine)

