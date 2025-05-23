from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import Reservation, Meeting, ProfessionalTopic, Class, RecurrentSchedule, SpecificSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent
from datetime import timedelta, datetime
from app.bd.bd_utils import error_hand, Schedule, include_time, include_time1, valid_time, strip_time_hour_minute
from app.bd.schemas import schema_prof
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific
from fastapi.responses import JSONResponse
from fastapi import status


class CreateRecurrent():
    @handle_errors
    def run(
        db: Session,
        recurrentR: Repository[RecurrentSchedule],
        meetingR: Repository[Meeting],
        professional_topicR: Repository[ProfessionalTopic],
        specificR: Repository[SpecificSchedule],
        classR: Repository[Class],
        recurrentS: schema_topic_recurrent.TopicRecurrentIn
    ):
        week_day = recurrentS.week_day
        start = strip_time_hour_minute(recurrentS.start)
        end = strip_time_hour_minute(recurrentS.end)

        if not week_day in range(0, 8):
            raise ValueError('Week is incorrect value')

        if recurrentS.topics <= 0:
           raise ValueError('Recurrent day need topics') 
 
        recurrent_valid = Schedule(start= start, end= end)

        
        if not valid_time(recurrent_valid):
            raise ValidationError('Hour format is incorrect')
        
        
        specific = specificR.getWeekSpecific(recurrentS.prof_id, 
                                                    recurrentS.week_day, 
                                                    recurrentS.start, 
                                                    recurrentS.end)
        
        
        if specific > 0:
            raise ValidationError('Time include in days')
        

        recurrent = recurrentR.get_by({
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day
        })

        

        for r in recurrent:
            if not (recurrent_valid.start >= r.end or recurrent_valid.end <= r.start):
                raise ValidationError('Time is include in Recurrent')

        
        topics = professional_topicR.getTopics(
            {
                'prof_id': recurrentS.prof_id
            }
        )        

        recurrent_data = {
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day,
            'start': recurrentS.start,
            'end': recurrentS.end
        }

        recurrentR.create(recurrent_data)

        available_topics = [topic.topic_name for topic in topics]
        recurrent_data.pop('end')
        
        for topic in recurrentS.topics:
            if topic.topic_name in available_topics:
                recurrent_data.update({'topic_name': topic.topic_name})
                recurrentR.addTopic(recurrent_data)
                
        
        