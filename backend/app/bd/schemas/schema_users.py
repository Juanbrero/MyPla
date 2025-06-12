from pydantic import BaseModel
from typing import Optional
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
    link_acceso: Optional[str] = None
    cvu_alumno: Optional[str] = None
    cvu_profesional: Optional[str] = None
    

#Respuesta get
class Users(UsersCreate):
    """
        - auth0_id: str
        - name: str
    """

    class Config:
        #Permite convertir desde SQLAlchemy (no dicts)
        orm_mode= True