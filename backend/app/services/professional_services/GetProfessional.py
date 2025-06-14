from sqlalchemy.orm import Session
from app.models import Professional
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic

class GetProfessional():
    @handle_errors
    def run(
        db:Session,
        prof_id: str,
        professionalR: Repository[Professional]
    ):
        professional = professionalR.get_by({'prof_id':prof_id})

        if len(professional) <= 0:
            raise NotFound('Professional not found')
        
        response = {'prof_id':professional[0].prof_id, 'score':professional[0].score}
        
        return JSONResponse(status_code= status.HTTP_200_OK, content= response)