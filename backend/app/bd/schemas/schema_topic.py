from pydantic import BaseModel
#Aqui van los esqueletos de respuestas que podran obtener


#Base esqueleto de datos minimos, sin datos generados por la BD o FK
class TopicBase(BaseModel):
    topic_name:str
    pass


#Create esquema utilizado para generar los datos a insertar
class TopicCreate(TopicBase):
    pass

#Respuesta get
class Topic(TopicBase):
    topic_name: str

    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True
