from fastapi import APIRouter, Depends
from app.bd.schemas import schema_reservation
from app.config.database import get_db
from sqlalchemy.orm import Session
from ..bd.bd_utils import Errors, Info
from typing import List, Union
from app.auth0.dependencies import RolesValidator
from ..controllers.ReservationController import ReservationController
from datetime import datetime

router = APIRouter(prefix="/api/reservation")


#Reserva una clase en un horario en base a la agenda del profesor
@router.post('/start-class',tags=["Reservation"], response_model=Union[schema_reservation.ReservationClassIn, Errors])
def reservation_class(class_:schema_reservation.ReservationClassCtrl, db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Alumno"]))):
    """
    Creacion de una clase
    """
    reservationS = schema_reservation.ReservationClassIn(**class_.dict(), student_id= user_info["user_id"])
    return ReservationController(db=db).createReservation(reservationS)


@router.put('/cancel')
def cancel_reservation(day_hour:datetime, user_id:str, user_cancel = Depends(RolesValidator(["Alumno", "Profesional"])), db: Session = Depends(get_db)):
    return ReservationController(db= db).cancelReservation(day_hour= day_hour, user_id= user_id, user_cancel= user_cancel["user_id"], role= user_cancel["roles"][0] )