from app.utils.errors import handle_errors, ValidationError, NotFound
from app.bd.schemas import schema_exception
from sqlalchemy.orm import Session
from app.models import Meeting, SpecificSchedule, RecurrentSchedule
from app.bd.repositories.Repository import Repository
from app.bd.bd_utils import strip_time_hour_minute
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import time

class CreateException:
    @handle_errors
    def run(
            db : Session, 
            exceptionS : schema_exception.ExceptionCreate, 
            exceptionR : Repository[SpecificSchedule],
            meetingR : Repository[Meeting],
            recurrentR: Repository[RecurrentSchedule]
    ):
        exceptionS.start = strip_time_hour_minute(exceptionS.start)
        exceptionS.end = strip_time_hour_minute(exceptionS.end)

        if exceptionS.start.minute != exceptionS.end.minute:
            raise ValidationError('Hour incomplete')
        
        if exceptionS.end.hour == 0:
            exceptionS.end = time(hour=23, minute=59)

        if exceptionS.start >= exceptionS.end:
            raise ValidationError('The range hour is invalid')
        
        exceptions = exceptionR.getSpecificsToRange(exceptionS.prof_id, exceptionS.day, exceptionS.start, exceptionS.end)

        if len(exceptions) > 0:
            raise ValidationError("In hour you have hour specific to disponibility or exception")
        
        recurrent = recurrentR.getException(
            {
                'prof_id': exceptionS.prof_id,
                'week': exceptionS.day.weekday(),
                'start': exceptionS.start,
                'end': exceptionS.end
            }
        )
        if len(recurrent) == 0:
            raise NotFound('Recurrent day not found')

        meetings = meetingR.getMeetingToRange(exceptionS.prof_id, exceptionS.day, exceptionS.start, exceptionS.end)
        if len(meetings) > 0:
            raise ValidationError("In hour you have a meeting")
        
        exceptionR.create(
            {
            "day": exceptionS.day,
            "start": exceptionS.start,
            "end": exceptionS.end,
            "prof_id": exceptionS.prof_id,
            "isCanceling": True
            }
        )

        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Exception created")