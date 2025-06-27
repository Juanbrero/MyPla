from app.bd.repositories.Repository import Repository
from app.models import Class, Professional

from fastapi.responses import JSONResponse
from app.utils.errors import handle_errors, NotFound
from fastapi import status
from sqlalchemy.orm import Session
from datetime import datetime
from app.bd.schemas import schema_calificate

class CalificateProfessional:
    @handle_errors
    def run(
        db: Session,
        classR: Repository[Class],
        professionalR: Repository[Professional],
        student_id: str,
        calificateS: schema_calificate.Calificate
    ):
        clase = classR.getClass(calificateS.prof_id, calificateS.day_hour, student_id)
        if clase is None:
            raise NotFound('Class to calificate not exist')

        if calificateS.score not in range(0, 6):
            raise ValueError('Score value invalid')

        
        updated = classR.update({'calificate_teacher':calificateS.score},
                      {
                          'prof_id': calificateS.prof_id,
                          'day_hour': calificateS.day_hour,
                          'calificate_teacher': None
                      })
        
        califications = classR.getCalificationProfessional(calificateS.prof_id)

        count, sum = califications
        professionalR.update({'score': sum/count}, {'prof_id': calificateS.prof_id})


        db.commit()

        return JSONResponse(status_code= status.HTTP_200_OK, content='Calification register')
