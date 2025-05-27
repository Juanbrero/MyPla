from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import  ProfessionalTopic, RecurrentSchedule, TopicRecurrent
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent

from app.bd.bd_utils import strip_time_hour_minute
from app.bd.schemas import schema_topic_recurrent

from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific

from fastapi.responses import JSONResponse
from fastapi import status
from datetime import time


class AddTopicRecurrent():
    @handle_errors
    def run(
        db: Session,
        topic_recurrentS: schema_topic_recurrent.TopicRecurrentIn,
        recurrentR: Repository[RecurrentSchedule],
        professional_topicR: Repository[ProfessionalTopic],
        topic_recurrentR: Repository[TopicRecurrent]
        
    ):
        if not topic_recurrentS.week_day in range(1, 8):
            raise ValidationError('Week value is invalid')

        topic_recurrentS.start = strip_time_hour_minute(topic_recurrentS.start)
        
        if len(topic_recurrentS.topics) == 0:
            raise ValidationError('Not topics to add')

        recurrent = recurrentR.get_by({
            'prof_id': topic_recurrentS.prof_id,
            'week_day': topic_recurrentS.week_day,
            'start': topic_recurrentS.start
        })
        
        if len(recurrent) == 0:
            raise NotFound('Recurrent day not found')
        

        prof_topics = professional_topicR.getTopics(topic_recurrentS.prof_id)
       
        for topic in topic_recurrentS.topics:
            if not topic in prof_topics:
                raise NotFound(f'{topic} not is from Professional')
            
        
            topic_recurrentR.create({
               'prof_id': topic_recurrentS.prof_id,
                'week_day': topic_recurrentS.week_day,
                'start': topic_recurrentS.start,
                'topic_name':topic 
            })
        
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content='Recurrent topics updated')