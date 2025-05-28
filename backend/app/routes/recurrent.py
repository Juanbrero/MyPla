from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from ..controllers.RecurrentController import RecurrentController
from app.bd.schemas import schema_topic_recurrent
from datetime import time


router = APIRouter(prefix="/recurrent")



@router.post('', tags=['Recurrent'])
def create_recurrent(prof_id: str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db: Session = Depends(get_db)):
    """
    Creacion de un dia recurrente
    """
    recurrentS = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    return RecurrentController(db= db).createRecurrent(recurrentS)

@router.get('', tags=['Recurrent'])
def get_recurre(prof_id: str, db: Session = Depends(get_db)):
    return RecurrentController(db= db).getRecurrentProf(prof_id)

"""
@router.get('', tags=['Recurrent'])
def get_week(prof_id:str, week_day: int, db: Session = Depends(get_db)):
    recurrentS = schema_topic_recurrent.TopicRecurrentWeekGet(prof_id= prof_id, week_day= week_day)
    return RecurrentController(db= db).getRecurrentWeek(recurrentS)
"""



@router.delete('', tags=['Recurrent'])
def del_recurrent(prof_id:str, week_day:int, start:time ,db: Session = Depends(get_db)):
    recurrentS = schema_topic_recurrent.TopicRecurrentSchema(prof_id= prof_id, week_day= week_day, start= start)
    return RecurrentController(db= db).delRecurrent(recurrentS)


@router.put('', tags=['Recurrent'])
def update_recurrent(prof_id:str, update:schema_topic_recurrent.TopicRecurrentUp, db: Session = Depends(get_db)):
    rescurrentS = schema_topic_recurrent.TopicRecurrentUpdate(**update.dict(), prof_id= prof_id)
    return RecurrentController(db= db).updateRecurrent(rescurrentS)