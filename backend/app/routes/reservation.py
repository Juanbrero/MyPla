from fastapi import APIRouter, Depends
from app.bd.schemas import schema_reservation
from app.config.database import get_db
from sqlalchemy.orm import Session
from ..bd.bd_utils import Errors, Info
from typing import List, Union
from app.auth0.dependencies import RolesValidator
from ..controllers.ReservationController import ReservationController


router = APIRouter(prefix="/api/reservation")


#Reserva una clase en un horario en base a la agenda del profesor
@router.post('/start-class',tags=["Reservation"], response_model=Union[schema_reservation.ReservationClassIn, Errors])
def reservation_class(class_:schema_reservation.ReservationClassCtrl, db:Session = Depends(get_db), user_info = Depends(RolesValidator(["Alumno"]))):
    """
    Creacion de una clase
    """
    reservationS = schema_reservation.ReservationClassIn(**class_.dict(), student_id= user_info["user_id"])
    return ReservationController(db=db).createReservation(reservationS)

@router.get('/student', response_model=schema_reservation.StudentReservation)
def student_reservation(user_info = Depends(RolesValidator(['Alumno'] ) ), db:Session= Depends(get_db) ):
    """
        Endpoint para solicitar todas las reservas pagadas de un alumno

            - Args:
                - token -> student_id
            - Returns:
                - {"reservations": [
                { "prof_id": str,
                "prof_id": str,
                "day_hour": datetime
                "topic":str
                }]}
    """
    return ReservationController(db= db).studentReservation(studen_id= user_info["user_id"])