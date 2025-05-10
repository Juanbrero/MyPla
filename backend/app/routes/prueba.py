from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from typing import List, Union
from app.bd.cruds import crud_user
from app.bd.bd_utils import Errors, Info


router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}

#MUESTRA DE SCHEMA RESPONSE
#En el body esta la respuesta al alumno
#En el response esta la respuesta al Professional
from ..bd.schemas import schema_response, schema_users
@router.post("/RESPONSE", 
             response_model=schema_response.ResponseProfessional, 
             tags=['TEST'], summary=" Endpoint para ver esquema de respuesta")
async def test(res:schema_response.Response):
    """
    On prueba
    Modelo de respuesta desde el back al Front:

     - Body: esquema para respuesta alumno 
     - Response: esquema para professional
    """
    return None

###
@router.post('/users',tags=["USER"], response_model=[schema_users.Users, Errors])
async def create_user(user: schema_users.UsersBase, db: Session = Depends(get_db)):
    """
    Insercion de un usuario
    - Falta ampliar información a recibir
    """
    user_insert = schema_users.UsersCreate(**user.dict(), name= user.user_id)
    return crud_user.add_user(db, user_insert)
        

@router.get('/users', tags=["USER"], response_model=List[schema_users.Users])
async def get_all(db:Session = Depends(get_db)):
    """
    Recuperación de todos los usuarios
    """
    return crud_user.get_users(db)

@router.delete('/users',tags=["USER"], response_model=Union[Info, Errors])
async def delete_user(user:schema_users.UsersBase, db:Session = Depends(get_db)):
    """
    Eliminacion de un usuarios
    """
    return crud_user.del_user(db, user)
    

###




