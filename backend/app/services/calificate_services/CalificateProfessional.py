from app.bd.repositories.Repository import Repository
from app.models import Class, Professional

from fastapi.responses import JSONResponse
from app.utils.errors import handle_errors, NotFound
from fastapi import status
from sqlalchemy.orm import Session
from datetime import datetime

class CalificateProfessional:
    @handle_errors
    def run(
        db: Session,
        classR: Repository[Class],
        professionalR: Repository[Professional],
        student_id: str,
        day_hour: datetime,
        prof_id: str,
        score: int
    ):
        clase = classR.getClass(prof_id, day_hour, student_id)
        if clase is None:
            raise NotFound('Class to calificate not exist')

        updated = classR.update({'calificate_teacher':score},
                      {
                          'prof_id': prof_id,
                          'day_hour': day_hour,
                          'calificate_teacher': None
                      })
        
        califications = classR.getCalificationProfessional(prof_id)

        count, sum = califications
        professionalR.update({'score': sum/count}, {'prof_id': prof_id})


        db.commit()

        return JSONResponse(status_code= status.HTTP_200_OK, content='Calification register')
