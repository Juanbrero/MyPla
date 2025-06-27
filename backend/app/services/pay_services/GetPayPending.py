from sqlalchemy.orm import Session
from app.models import Reservation, Meeting, Class, Cancelation
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic
from datetime import datetime, timedelta
# SDK de Mercado Pago
from os import getenv
import mercadopago
# Agrega credenciales (private key)
sdk = mercadopago.SDK(getenv("ACCESS_TOKEN_MP"))


class GetPayPending:
    @handle_errors
    def run (
        reservationR: Repository[Reservation],
        cancelationR: Repository[Cancelation]
    ):
        reservations = reservationR.getReservationsForTransaction()
        reservData = []
        for reservation, professional, student, prof_email, stud_email ,price in reservations:
            print(stud_email)
            rData = {
                "type": 'pay' ,
                "price": price,
                "cvu": professional.cvu ,
                "day_hour": reservation.day_hour.isoformat(),
                "user_student": {
                    "student_id": student.student_id,
                    "email": stud_email
                },
                "user_professional": {
                    "professional_id": professional.prof_id,
                    "email": prof_email
                }
            }
            reservData.append(rData)

        response = []
        index_reserv = 0
        cancelation = cancelationR.getCancelations()
        
        for cancel, professional, student, prof_email, stud_email in cancelation:
            found = False

            for reserv in range(index_reserv, len(reservData)):
                if reservData[reserv]['day_hour'] <= cancel.cancel_time.isoformat():
                    
                    response.append(reservData[reserv])
                else:
                    rData={
                        "type": 'refund',
                        "price": cancel.price,
                        "cvu": student.cvu,
                        "day_hour": cancel.day_hour.isoformat(),
                        "user_student": {
                            "student_id": student.student_id,
                            "email": stud_email
                        },
                        "user_professional": {
                            "professional_id": professional.prof_id,
                            "email": prof_email
                        },
                        "day_hour_cancel": cancel.cancel_time.isoformat()
                    }
                    response.append(rData)
                    index_reserv = reserv
                    found = True
                    break

            if not found :
                rData={
                        "type": 'refund',
                        "price": cancel.price,
                        "cvu": student.cvu,
                        "day_hour": cancel.day_hour.isoformat(),
                        "user_student": {
                            "student_id": student.student_id,
                            "email": stud_email
                        },
                        "user_professional": {
                            "professional_id": professional.prof_id,
                            "email": prof_email
                        },
                        "day_hour_cancel": cancel.cancel_time.isoformat()
                    }
                
                response.append(rData)
                index_reserv = len(reservData)
        
        if index_reserv < len(reservData):
            response.extend(reservData[index_reserv:])
        

        return JSONResponse(status_code=status.HTTP_200_OK, content=response)