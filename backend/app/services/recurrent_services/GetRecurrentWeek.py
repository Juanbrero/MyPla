from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import RecurrentSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent

from fastapi.responses import JSONResponse
from fastapi import status


class GetRecurrentWeek():
    @handle_errors
    def run(
        db:Session,
        recurrentS: schema_topic_recurrent.TopicRecurrentWeekGet,
        recurrentR: Repository[RecurrentSchedule]
    ):

        
        if not recurrentS.week_day in range(0, 8):
            raise ValueError('Week value is incorrect')

        response = recurrentR.getRecurrentsWithTopics(recurrentS.prof_id)
        
      
        respuesta = [ 
            schema_topic_recurrent.TopicRecurrentCr1(week_day= recu.week_day,
                                                     start= recu.start,
                                                     end= recu.end,
                                                     topics=[topic.topic_name for topic in recu.topic_recurrents]).dict() 
            for recu in response if recu.week_day == recurrentS.week_day 
            ]
        
        return respuesta

