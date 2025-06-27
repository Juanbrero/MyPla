from app.bd.repositories.Repository import Repository
from app.models import Class

from fastapi.responses import JSONResponse
from app.utils.errors import handle_errors, NotFound
from fastapi import status
from sqlalchemy.orm import Session

class GetCalification:
    @handle_errors
    def run(
        db: Session,
        id: str,
        role: str,
        classR: Repository[Class]
    ):
        if role == 'Alumno':
            result = classR.getCalificateProfessional(id)
        else:
            result = classR.getCalificateStudent(id)

        response = []
        for clase, username, topic in result:
            item = {
                'prof_id': clase.prof_id,
                'day_hour': clase.day_hour.isoformat(),
                "prof_username": username,
                "topic": topic
            }
            response.append(item)

        return JSONResponse(status_code= status.HTTP_200_OK, content={'calificate': response})