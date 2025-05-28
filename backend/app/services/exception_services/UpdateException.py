from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from sqlalchemy.orm import Session
from app.bd.repositories.Repository import Repository
from app.models import SpecificSchedule, Meeting
from fastapi.responses import JSONResponse
from fastapi import status
from app.bd.schemas import schema_exception
from app.bd.bd_utils import strip_time_hour_minute
from datetime import time


class UpdateExceptions():
    @handle_errors
    def run(
        db : Session, 
        exceptionS : schema_exception.ExceptionUpdate,
        exceptionR : Repository[SpecificSchedule], 
        meetingR : Repository[Meeting]
    ):
        #si no hay nada para actualizar
        if not (exceptionS.Nday or exceptionS.Nend or exceptionS.Nstart):
            raise NotFound('Not update information')
        
        old_exception = exceptionR.get_by({
            "day": exceptionS.day,
            "start": exceptionS.start,
            "isCanceling": True
        })
        
        if (len(old_exception) <= 0):
            raise NotFound("Exception disponibility not exist")
        
               
        start = exceptionS.Nstart if exceptionS.Nstart else exceptionS.start
        day = exceptionS.Nday if exceptionS.Nday else exceptionS.day
        end = exceptionS.Nend if exceptionS.Nend else old_exception[0].end

        start = strip_time_hour_minute(start)
        end = strip_time_hour_minute(end)
        
        

        if start.minute != end.minute:
            raise ValidationError('Hour incomplete')

        if end.hour == 0:
            end = time(hour=23, minute=59)

        if start >= end:
            raise ValidationError("The range hour is invalid")
        
        
        exceptions = exceptionR.getexceptionsToRange(exceptionS.prof_id, day, start, end)
        # Valido si existe otro exception en el rango, en caso de que haya uno deberia chequear si no es el mismo que envio el usuario 
        if len(exceptions) > 1 or (len(exceptions) == 1 and (exceptionS.day != exceptions[0].day or exceptionS.start != exceptions[0].start)):
            raise ValidationError("In hour you have hour specific to disponibility or exception")
        
        meetings = meetingR.getMeetingToRange(exceptionS.prof_id, day, start, end)
        if len(meetings) > 0:
            raise ValidationError("In hour you have a meeting")
        
        exceptionR.update({
            "day": day,
            "start": start,
            "end": end
        }, {
            "day": exceptionS.day,
            "start": exceptionS.start,
            "prof_id": exceptionS.prof_id,
        })
    
            
        
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content="Exception modified")