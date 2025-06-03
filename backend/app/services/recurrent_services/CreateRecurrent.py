from app.utils.errors import handle_errors, ValidationError
from app.models import ProfessionalTopic, RecurrentSchedule, TopicRecurrent
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent

from app.bd.bd_utils import Schedule, strip_time_hour_minute
from app.bd.schemas import schema_topic_recurrent

from fastapi.responses import JSONResponse
from fastapi import status
from datetime import time

class CreateRecurrent():
    @handle_errors
    def run(
        db: Session,
        recurrentS: schema_topic_recurrent.TopicRecurrentIn,
        recurrentR: Repository[RecurrentSchedule],
        professional_topicR: Repository[ProfessionalTopic],
        topic_recurrentR: Repository[TopicRecurrent]
        
    ):
        
        if not recurrentS.week_day in range(0, 7):
            raise ValueError('Week value is invalid')
        
        
        if len(recurrentS.topics) == 0:
            raise ValidationError("You don't have a topic")
        

        recurrentS.start = strip_time_hour_minute(recurrentS.start)
        recurrentS.end = strip_time_hour_minute(recurrentS.end)
        
        
        recurrent_valid = Schedule(start= recurrentS.start, end= recurrentS.end)

        if recurrentS.start.minute != recurrentS.end.minute:
            raise ValidationError('Hour incomplete')
        
        # Conversion de hora fin 0 a 23:59, para comparaciones y almacenado, 0 < all 
        if recurrentS.end.hour == 0:
            recurrentS.end = time(hour=23, minute=59)
        
        if recurrentS.start >= recurrentS.end:
            raise ValidationError('The range hour is invalid')
        
        
    
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
        
        prof_topics = professional_topicR.getTopics(recurrentS.prof_id)

        if not professional_topicR.checkTopicProf(recurrentS.prof_id, recurrentS.topics):
            raise ValidationError("You don't have a topic")
        
        for topic in recurrentS.topics:
            topic_recurrentR.create({
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day,
            'start': recurrentS.start,
            'topic_name': topic
        }
                
            )

        

        db.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Recurrent created")
        
        