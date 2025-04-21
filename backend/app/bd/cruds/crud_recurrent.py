from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.RecurrentSchedule import RecurrentSchedule
from app.bd.schemas import schema_recurrent
#Aqui se crearan las funciones que utilizaran los esquemas y modelos
from datetime import date
from app.bd.bd_utils import strip_time_hour_minute


def get_all_recurrent(db: Session, user_id:int):
    smt = select(RecurrentSchedule).where(RecurrentSchedule.user_id == user_id)
    response = db.scalars(smt).all()
    return response


def create_recurrent(db: Session, recurrent: schema_recurrent.RecurrentCreate, id_prof:int):
    recurrent.start = strip_time_hour_minute(recurrent.start)
    recurrent.end = strip_time_hour_minute(recurrent.end)
    try:
        db_spec = RecurrentSchedule(**recurrent.dict(), user_id=id_prof)
        db.add(db_spec)
        db.commit()
        db.refresh(db_spec)
    except:
        db_spec = {'Error':'on create_spec'}
    return db_spec
