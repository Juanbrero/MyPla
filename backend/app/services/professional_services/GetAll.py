from sqlalchemy.orm import Session
from app.models import Professional
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof

class GetAll():
    @handle_errors
    def run(
        db: Session,
        professionalR: Repository[Professional],
    ):
        profesionales = professionalR.getProfessionals()


        response = []
        for prof_id, prof_username in profesionales:
            prof = schema_prof.ProfessionalInfo(
                prof_id= prof_id,
                prof_username= prof_username
            )
            response.append(prof.dict())

        return JSONResponse(status_code= status.HTTP_200_OK, content= {"professionals":response})