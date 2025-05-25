from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import  Meeting, ProfessionalTopic, RecurrentSchedule, SpecificSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent
from datetime import timedelta
from app.bd.bd_utils import error_hand, Schedule, include_time, include_time1, valid_time, strip_time_hour_minute
from app.bd.schemas import schema_topic_recurrent

from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific

from fastapi.responses import JSONResponse
from fastapi import status
from datetime import time

class CreateRecurrent():
    @handle_errors
    def run(
        db: Session,
        recurrentS: schema_topic_recurrent.TopicRecurrentIn,
        recurrentR: Repository[RecurrentSchedule],
        meetingR: Repository[Meeting],
        professional_topicR: Repository[ProfessionalTopic]
        
    ):
        
        if not recurrentS.week_day in range(1, 8):
            raise ValueError('Week is incorrect value')
        

        recurrentS.start = strip_time_hour_minute(recurrentS.start)
        recurrentS.end = strip_time_hour_minute(recurrentS.end)
        
        
        recurrent_valid = Schedule(start= recurrentS.start, end= recurrentS.end)

        
        if not valid_time(recurrent_valid):
            raise ValidationError('Hour format is incorrect')
        
        # Conversion de hora fin 0 a 23:59, para comparaciones y almacenado, 0 < all 
        if recurrentS.end.hour == 0:
            recurrentS.end = time(hour=23, minute=59)
        
        meetings = meetingR.getMeetingRecurrent(recurrentS.prof_id, recurrentS.week_day, recurrentS.start, recurrentS.end)

        if len(meetings) > 0:
            raise ValidationError("In hour you have a meeting")
        
        recurrent = recurrentR.get_by({
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day
        })

        
        for r in recurrent:
            if not (recurrent_valid.start >= r.end or recurrent_valid.end <= r.start):
                raise ValidationError('Time is include in Recurrent')
 

        recurrentR.create({
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day,
            'start': recurrentS.start,
            'end': recurrentS.end
        }

        )

        db.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Recurrent created")
        
        