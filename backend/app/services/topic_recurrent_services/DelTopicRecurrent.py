from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import  ProfessionalTopic, RecurrentSchedule, TopicRecurrent
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent

from app.bd.bd_utils import strip_time_hour_minute


from fastapi.responses import JSONResponse
from fastapi import status



class DelTopicRecurrent():
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
            raise ValidationError('Not topics to delete')

        recurrent = recurrentR.get_by({
            'prof_id': topic_recurrentS.prof_id,
            'week_day': topic_recurrentS.week_day,
            'start': topic_recurrentS.start
        })

        if len(recurrent) == 0:
            raise NotFound('Recurrent day not found')
        

        recurrent = topic_recurrentR.get_by({
            'prof_id':topic_recurrentS.prof_id,
            'week_day':topic_recurrentS.week_day,
            'start':topic_recurrentS.start}
            )
        
        recurrent_topics_len = len(recurrent)

        for topic in recurrent:
            if topic.topic_name in topic_recurrentS.topics:
                topic_recurrentR.delete(
                    {
                        'prof_id':topic_recurrentS.prof_id,
                        'week_day':topic_recurrentS.week_day,
                        'start':topic_recurrentS.start,
                        'topic_name': topic.topic_name
                    }
                )
                recurrent_topics_len -= 1

        if recurrent_topics_len <= 0:
            db.rollback()
            raise ValidationError('Delete all topics not possible')    
        
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content='Recurrent topics deleted')