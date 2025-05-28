from app.utils.errors import handle_errors
from sqlalchemy.orm import Session
from app.bd.repositories.Repository import Repository
from app.models import SpecificSchedule
from fastapi.responses import JSONResponse
from fastapi import status

class GetSpecifics:
    @handle_errors
    def run (
        db: Session,
        prof_id: str,
        specificR: Repository[SpecificSchedule]
    ):
        all_specifics = specificR.getAllWithTopics(prof_id, False)
        data = []
        for schedule in all_specifics:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat(),
                "topics": [topic.topic_name for topic in schedule.topic_specifics]
            }
            data.append(item)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"specifics": data})
        