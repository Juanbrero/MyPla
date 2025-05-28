from pydantic import BaseModel
#Aqui van los esqueletos de respuestas que podran obtener


#Base esqueleto de datos minimos, sin datos generados por la BD o FK
class TopicBase(BaseModel):
    """
    Esquema de topic
        - topic_name: str
    """
    topic_name: str



#Create esquema utilizado para generar los datos a insertar
class TopicCreate(TopicBase):
    """
    Esquema para la creación de topicos
         - topic_name: str
    """
    pass

#Respuesta get
class Topic(TopicBase):
    """
    Esquema para la respuesta de topicos
         - topic_name: str
    """
    topic_name: str

    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True
