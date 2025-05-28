from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import RecurrentSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent

from fastapi.responses import JSONResponse
from fastapi import status


class GetRecurrentProf():
    @handle_errors
    def run(
        db:Session,
        prof_id: str,
        recurrentR: Repository[RecurrentSchedule]
    ):
        all_recurrent = recurrentR.get_by({'prof_id':prof_id})


        data = []
        for recurrent in all_recurrent:
            item = {"week_day": recurrent.week_day,
            "start": recurrent.start.isoformat(),
            "end": recurrent.end.isoformat(),
            "topics":[topic.topic_name for topic in recurrent.topic_recurrents]
            }
            data.append(item)
    
        return JSONResponse(status_code=status.HTTP_200_OK, content={"recurrent": data})