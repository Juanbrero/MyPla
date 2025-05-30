from fastapi import APIRouter, Depends
from app.bd.schemas import schema_users
from app.config.database import get_db
from sqlalchemy.orm import Session
from ..bd.bd_utils import Errors, Info
from typing import List, Union
from ..controllers.UserController import UserController


router = APIRouter(prefix="/api/user")


#Reserva una clase en un horario en base a la agenda del profesor
@router.post('',tags=["User"], response_model=Union[schema_users.UsersCreate, Errors])
def create_user(user:schema_users.UsersCreate, db:Session = Depends(get_db)):
    """
    Creacion de una clase
    """
    userS = schema_users.UsersCreate(**user.dict())
    return UserController(db=db).createUser(userS)