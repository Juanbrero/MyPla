from app.utils.errors import handle_errors, NotFound
from app.models import RecurrentSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent
from app.bd.bd_utils import strip_time_hour_minute
from fastapi.responses import JSONResponse
from fastapi import status



class DelRecurrent():
    @handle_errors
    def run(
        db:Session,
        recurrentS: schema_topic_recurrent.TopicRecurrentSchema,
        recurrentR: Repository[RecurrentSchedule] 
    ):
        if not recurrentS.week_day in range(1, 8):
            raise ValueError('Week value is invalid')
        
        recurrentS.start = strip_time_hour_minute(recurrentS.start)
        deleted = recurrentR.delete(recurrentS.dict())
        
        if deleted == 0:
            raise NotFound('Recurrent day not exist')
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content='Recurrent deleted')