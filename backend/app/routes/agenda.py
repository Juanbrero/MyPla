from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date, time

from app.bd.schemas.schema_specific import Specific, SpecificCreate, SpecificIsCancel
from app.bd.schemas.schema_recurrent import Recurrent, RecurrentCreate
import app.models as models
from app.bd.cruds import crud_specific, crud_recurrent
from app.bd.schemas.schema_prof_topic import ProfesionalTopic
from app.bd.schemas.schema_topic import Topic
from app.bd.bd_utils import Errors

router = APIRouter(prefix="/prof/{prof_id}/agenda", tags=["Agenda"])

#trae todos los dias sin filtro 
@router.get("/list/specificday",
            response_model=List[Specific],
            tags=["Specific"])
async def get_all_dias(db: Session = Depends(get_db)):
    return crud_specific.get_all_specific(db)

#Crea un dia especifico para un profesional
@router.post("/create/specificday", 
             response_model=Union[Specific, Errors], 
             tags=["Specific"])
async def create_dia(dia: SpecificCreate,
                prof_id: int, 
                db: Session= Depends(get_db)):
    return crud_specific.create_specific(db, dia, prof_id)

#Consulta el estado del dia y hora, si esta o no cancelado
@router.get("/specif/{day}/state",
            response_model=List[SpecificIsCancel],
            tags=["Specific"])
async def isCaceled( prof_id:int, day:date, hour:time, db: Session = Depends(get_db)):
    return crud_specific.iscaceled_specific(db, day, prof_id, hour)

#Actualiza el estado a cancelado
@router.put("/specif/{day}/cancel",tags=["Specific"])
async def cancel(prof_id:int, day:date, hour:time, db: Session = Depends(get_db)):
    return crud_specific.cancel_day(db, prof_id, day, hour)

#Recupera todos los horarios de un profesional especificado
@router.get("/all/specific",
            response_model=List[Specific],
            tags=["Specific"])
async def get_day(prof_id:int, db: Session = Depends(get_db)):
    return crud_specific.get_day(db, prof_id)



@router.get("/list/recurrent", 
            response_model=List[Recurrent],
              tags=["Recurrent"])
async def get_dias(prof_id:int, db: Session = Depends(get_db)):
    return crud_recurrent.get_all_recurrent(db, prof_id)

@router.post("/create/recurent", 
             response_model=Union[Recurrent, Errors], 
             tags=["Recurrent"])
async def create_recurrent(dia: RecurrentCreate, prof_id: int, db: Session = Depends(get_db)):
    return crud_recurrent.create_recurrent(db, dia, prof_id)

@router.get("/day/{name_day}",
            response_model=Union[List[Recurrent],Errors],
            tags=["Recurrent"])
async def get_day(prof_id:int, name_day:str, db: Session = Depends(get_db)):
    return crud_recurrent.get_day(db, prof_id, name_day)
