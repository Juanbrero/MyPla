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
            raise ValueError('Week value is invalid')

        response = recurrentR.getRecurrentsWithTopics(recurrentS.prof_id)

        data = []
        for recurrent in response:
            if recurrent.week_day == recurrentS.week_day:
                item = {"week_day": recurrent.week_day,
                "start": recurrent.start.isoformat(),
                "end": recurrent.end.isoformat(),
                "topics":[topic.topic_name for topic in recurrent.topic_recurrents]
                }
                data.append(item)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"recurrent": data})

