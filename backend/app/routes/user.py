from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union
from app.bd.schemas import schema_users

from app.bd.bd_utils import Errors, Info
from app.bd.cruds.crud_user import UserRepository
from sqlalchemy.orm import Session
from app.config.database import get_db

router = APIRouter()

@router.post('/users',tags=["USER"])
def create_user(user: schema_users.UsersBase, db: Session = Depends(get_db)):
    """
    Insercion de un usuario
    - Falta ampliar información a recibir
    """
    user_insert = schema_users.UsersCreate(**user.dict(), name= user.user_id)
    repository = UserRepository(db)
    db_user = repository.get_user_id(user_insert)
    if not db_user is None:
        raise HTTPException(status_code=400, detail='User already exist')
    return repository.add_user(user_insert)
        

@router.get('/users', tags=["USER"])
def get_all(db:Session = Depends(get_db)):
    """
    Recuperación de todos los usuarios
    """
    repository = UserRepository(db)
    return repository.get_users()

@router.get('/users/{user_id}', tags=['USER'])
def get_user(user_id:str, db: Session = Depends(get_db)):
    user = schema_users.UsersBase(user_id=user_id)
    repository = UserRepository(db)
    response = repository.get_user_id(user)
    if response is None:
        raise HTTPException(status_code=404, detail='User not found')
    return response

@router.delete('/users/{user}',tags=["USER"])
def delete_user(user:str, db:Session = Depends(get_db)):
    """
    Eliminacion de un usuarios
    """
    user_del = schema_users.UsersBase(user_id=user)
    repository = UserRepository(db)
    sucess = repository.del_user(user_del)
    if not sucess:
        raise HTTPException(status_code=404, detail='User not found')
    return {'detail': 'User deleted sucessfully'}

