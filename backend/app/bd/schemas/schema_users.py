from pydantic import BaseModel
#Aqui van los esqueletos de respuestas que podran obtener


#Base esqueleto de datos minimos, sin datos generados por la BD o FK
class UsersCreate(BaseModel):
    """
        - auth0_id: str
    """
    auth0_id: str
    email: str
    username: str
    role: str
    

#Respuesta get
class Users(UsersCreate):
    """
        - auth0_id: str
        - name: str
    """

    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True