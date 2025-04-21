from pydantic import BaseModel
#Aqui van los esqueletos de respuestas que podran obtener


#Base esqueleto de datos minimos, sin datos generados por la BD o FK
class Base(BaseModel):
    pass


#Create esquema utilizado para generar los datos a insertar
class Create(Base):
    pass

#Respuesta get
class SCHEMA(Base):

    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True
