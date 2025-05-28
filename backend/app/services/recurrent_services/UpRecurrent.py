from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import RecurrentSchedule, ProfessionalTopic, TopicRecurrent
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent
from datetime import timedelta
from app.bd.bd_utils import error_hand, Schedule, include_time, include_time1, valid_time, strip_time_hour_minute
from app.bd.schemas import schema_prof
from app.bd.cruds import crud_topic_recurrent
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import time

class UpRecurrent():
    @handle_errors
    def run(
        db:Session,
        recurrentS: schema_topic_recurrent.TopicRecurrentUpdate,
        recurrentR: Repository[RecurrentSchedule],
        professional_topicR: Repository[ProfessionalTopic],
        topic_recurrentR: Repository[TopicRecurrent]
        ):
        
        if not recurrentS.week_day in range(1, 8):
            raise ValueError('Week value is invalid')
        
        if not (recurrentS.Nstart or recurrentS.Nend or recurrentS.topics):
            raise ValidationError('Not update information')
        
        recurrentS.start = strip_time_hour_minute(recurrentS.start)

        query = {
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day,
            'start': recurrentS.start
        }

        obj_to_update = recurrentR.get_by(
            query
        )
        
      
        if len(obj_to_update) == 0:
            raise NotFound('Recurrent not found')
        
        update = {
            'start': strip_time_hour_minute(nstart) if (nstart := recurrentS.Nstart) is not None else obj_to_update[0].start,
            'end': strip_time_hour_minute(nend) if (nend := recurrentS.Nend) is not None else obj_to_update[0].end
        }
        
        if update['start'].minute != update['end'].minute:
            raise ValidationError('Hour incomplete')

        if update['end'].hour == 0:
            update['end'] = time(hour=23, minute=59)


        if update['start'] >= update['end']:
            raise ValueError('The range hour is invalid')
        
        
        list_week = recurrentR.getOmmit(
            query
        )

        for r in list_week:
            if not(update['end'] <= r.start or update['start'] >= r.end):
                raise ValidationError('Time is include in Recurrents')
        
        updated = recurrentR.update(update, query)

        

        if recurrentS.topics:

            prof_topics = professional_topicR.getTopics(recurrentS.prof_id)

            if not professional_topicR.checkTopicProf(recurrentS.prof_id, recurrentS.topics):
                raise ValidationError("You don't have a topic")
                        

            topic_names = {top.topic_name for top in obj_to_update[0].topic_recurrents}
            
            topic_del = [topic for topic in topic_names if topic not in recurrentS.topics]

            topic_add = [topic for topic in recurrentS.topics if topic not in topic_names]

           

            for topic in topic_del:
                topic_recurrentR.delete(
                    {
                       'prof_id':recurrentS.prof_id,
                        'week_day':recurrentS.week_day,
                        'start':update['start'],
                        'topic_name': topic 
                    }
                )
            
            for topic in topic_add:
                topic_recurrentR.create({
                    'prof_id': recurrentS.prof_id,
                    'week_day': recurrentS.week_day,
                    'start': update['start'],
                    'topic_name':topic  }
                    
                )
           


        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content='Recurrent updated')

        
