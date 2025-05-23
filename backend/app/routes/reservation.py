from fastapi import APIRouter, Depends
from app.bd.schemas import schema_reservation
from app.config.database import get_db
from sqlalchemy.orm import Session
from ..bd.bd_utils import Errors, Info
from typing import List, Union
from app.bd.cruds import crud_reservation
from ..controllers.ReservationController import ReservationController


router = APIRouter(prefix="/reservation")


#Reserva una clase en un horario en base a la agenda del profesor
@router.post('/class',tags=["Reservation"], response_model=Union[schema_reservation.ReservationClassIn, Errors])
def reservation_class(student_id: str, class_:schema_reservation.ReservationClassCtrl, db:Session = Depends(get_db)):
    """
    Creacion de una clase
    """
    reservationS = schema_reservation.ReservationClassIn(**class_.dict(), student_id= student_id)
    return ReservationController(db=db).createReservation(reservationS)