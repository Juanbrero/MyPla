from app.utils.errors import handle_errors
from sqlalchemy.orm import Session
from app.bd.repositories.Repository import Repository
from app.models import SpecificSchedule
from fastapi.responses import JSONResponse
from fastapi import status

class GetExceptions:
    @handle_errors
    def run (
        db: Session,
        prof_id: str,
        exceptionR: Repository[SpecificSchedule]
    ):
        all_exceptions = exceptionR.getAllWithProfessional(prof_id)
        data = []
        for schedule in all_exceptions:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat()
            }
            data.append(item)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"exceptions": data})
        