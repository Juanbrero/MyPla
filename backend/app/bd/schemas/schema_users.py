from pydantic import BaseModel
#Aqui van los esqueletos de respuestas que podran obtener


#Base esqueleto de datos minimos, sin datos generados por la BD o FK
class UsersBase(BaseModel):
    """
        - user_id: str
    """
    user_id: str


#Create esquema utilizado para generar los datos a insertar
class UsersCreate(UsersBase):
    """
        - user_id: str
        - name: str
    """
    name: str

#Respuesta get
class Users(UsersCreate):
    """
        - user_id: str
        - name: str
    """

    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True