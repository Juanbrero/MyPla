from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from sqlalchemy.orm import Session
from app.bd.repositories.Repository import Repository
from app.models import SpecificSchedule
from fastapi.responses import JSONResponse
from fastapi import status

from app.bd.schemas import schema_exception
from app.bd.bd_utils import strip_time_hour_minute
from datetime import time

class DeleteException():
    @handle_errors
    def run (
        db : Session, 
        exceptionS : schema_exception.ExceptionDelete, 
        exceptionR : Repository[SpecificSchedule]
    ):
        start = strip_time_hour_minute(exceptionS.start)

        exception = exceptionR.get_by({
       "day": exceptionS.day,
       "start": start,
       "isCanceling": True,
       "prof_id": exceptionS.prof_id
        })

        if (len(exception) <= 0):
            raise NotFound("Exception day hour not exist")
        
        exceptionR.delete({
            "day": exceptionS.day,
            "start": start,
            "isCanceling": True,
            "prof_id": exceptionS.prof_id
            }
        )

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content="Exception deleted")