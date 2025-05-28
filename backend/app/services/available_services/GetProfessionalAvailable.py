from app.utils.errors import handle_errors
from app.models import SpecificSchedule, Class, RecurrentSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status

class GetProfessionalAvailable():
    @handle_errors
    def run(
            db : Session,
            prof_id= str,
            recurrentR= Repository[RecurrentSchedule],
            exceptionR= Repository[SpecificSchedule],
            specificR= Repository[SpecificSchedule],
            classR= Repository[Class]
    ):
        all_specifics = specificR.getAllWithTopics(prof_id, False)

        all_exceptions = exceptionR.getAllWithProfessional(prof_id)
        
        all_recurrents = recurrentR.getRecurrentsWithTopics(prof_id)

        data_specific = []
        for schedule in all_specifics:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat(),
                "topics": [topic.topic_name for topic in schedule.topic_specifics]
            }
            data_specific.append(item)

        data_recurrent = []
        for schedule in all_recurrents:
            item = {
                "prof_id": schedule.prof_id,
                "week_day": schedule.week_day,
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat(),
                "topics": [topic.topic_name for topic in schedule.topic_recurrents]
            }
            data_recurrent.append(item)

        data_exception = []
        for schedule in all_exceptions:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat()
            }
            data_exception.append(item)
        
        response = {
            'specific': data_specific,
            'recurrent': data_recurrent,
            'exception': data_exception,
            'class': [],
            'event': []
        }

        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
        
