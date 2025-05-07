from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
#Imports to insert in BD
from sqlalchemy import insert
from app.models.User import User 



router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}


###
@router.post('/create/{user_id}',tags=["USER"])
def create_user(user_id: str, db: Session = Depends(get_db)):
    """
    Insercion de un usuario
    - Falta ampliar información a recibir
    """
    try:
        user = {'user_id': user_id, 'name':user_id}
        smt =insert(User).values(user)
        response = db.execute(smt)
        db.commit()
        return user
    except:
        return {'error':'en la insercion'}

@router.get('/get/all', tags=["USER"])
def get_all(db:Session = Depends(get_db)):
    """
    Recuperación de todos los usuarios
    """
    ic(f'GET USER')
    return db.query(User).all()

@router.delete('/delete/{user_id}',tags=["USER"])
def delete_user(user_id:str, db:Session = Depends(get_db)):
    """
    Eliminacion de un usuarios
    """
    try:
        res = db.get(User, user_id)
        db.delete(res)
        db.commit()
        return {'OK':'OK'}
    except:
        return {'error': 'not delete'}

###

#MUESTRA DE SCHEMA RESPONSE
#En el body esta la respuesta al alumno
#En el response esta la respuesta al Professional
from ..bd.schemas import schema_response
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


