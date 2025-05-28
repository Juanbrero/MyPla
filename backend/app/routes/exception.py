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

router = APIRouter(prefix="/exceptions")


@router.post('', tags=['Exception'])
def create_exception(prof_id: str, excep: schema_exception.ExceptionBase, db: Session = Depends(get_db)):
    exceptionS = schema_exception.ExceptionCreate(**excep.dict(), prof_id= prof_id)
    return ExceptionController(db= db).createException(exceptionS)

@router.get('', tags=['Exceptions'], response_model=schema_response.ResponseException)
def get_exception(prof_id: str, db: Session = Depends(get_db)):
    return ExceptionController(db= db).getException(prof_id)

@router.put('', tags=['Exceptions'])
def update_exception(prof_id:str, update:schema_exception.ExceptionUpInfo, db: Session = Depends(get_db)):
    exceptionS = schema_exception.ExceptionUpdate(**update.dict(), prof_id= prof_id)
    return ExceptionController(db= db).updateException(exceptionS)

@router.delete('', tags=['Exceptions'])
def delete_exception(prof_id: str, delete:schema_exception.ExceptionDel, db:Session = Depends(get_db)):
    exceptionS = schema_exception.ExceptionDelete(**delete.dict(), prof_id= prof_id)
    return ExceptionController(db= db).deleteException(exceptionS)

