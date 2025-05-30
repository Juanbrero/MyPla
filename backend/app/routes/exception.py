from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date, time

from app.bd.schemas import schema_exception
from ..controllers.ExceptionController import ExceptionController

from app.bd.schemas import schema_response, schema_prof

from app.bd.bd_utils import Errors, Info
from app.auth0.dependencies import RolesValidator

router = APIRouter(prefix="/api/exception")


@router.post('', tags=['Exceptions'])
def create_exception(excep: schema_exception.ExceptionBase, db: Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    exceptionS = schema_exception.ExceptionCreate(**excep.dict(), prof_id= user_info["user_id"])
    return ExceptionController(db= db).createException(exceptionS)

@router.get('', tags=['Exceptions'], response_model=schema_response.ResponseException)
def get_exception(db: Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    return ExceptionController(db= db).getException(user_info["user_id"])

@router.put('', tags=['Exceptions'])
def update_exception(update:schema_exception.ExceptionUpInfo, db: Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    exceptionS = schema_exception.ExceptionUpdate(**update.dict(), prof_id= user_info["user_id"])
    return ExceptionController(db= db).updateException(exceptionS)

@router.delete('', tags=['Exceptions'])
def delete_exception(delete:schema_exception.ExceptionDel, db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Profesional"]))):
    exceptionS = schema_exception.ExceptionDelete(**delete.dict(), prof_id= user_info["user_id"])
    return ExceptionController(db= db).deleteException(exceptionS)

