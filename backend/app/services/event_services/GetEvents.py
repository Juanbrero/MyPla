from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.bd.schemas import schema_event
from app.bd.repositories.Repository import Repository
from datetime import datetime, timedelta
from app.models import Meeting, SpecificSchedule, RecurrentSchedule, Invite, Event, Professional, Topic
from fastapi import status

class GetEvents:
    @handle_errors
    def run (
        db: Session,
        eventS: schema_event.EventGet,
        eventR: Repository[Event]
    ):
        events = eventR.getEventsPage(page=eventS.page, amount=eventS.amount)
        eventos_dict = {}
        
        for event, invite, user, creator in events:
            key = (event.prof_id, event.day_hour)
            if key not in eventos_dict:
                eventos_dict[key] = {
                    "prof_id": event.prof_id,
                    "day_hour": event.day_hour.isoformat(),
                    "duration": event.duration,
                    "price": event.price,
                    "confirm": event.confirm,
                    "cancel": event.cancel,
                    "creator": creator.username,
                    "invites": []
                }
            if user:
                eventos_dict[key]["invites"].append(user.username)

        eventos_finales = list(eventos_dict.values())
        return JSONResponse(status_code=status.HTTP_200_OK, content=eventos_finales)