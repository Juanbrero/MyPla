from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.bd.schemas import schema_event
from app.bd.repositories.Repository import Repository
from datetime import datetime, timedelta
from app.models import Meeting, SpecificSchedule, RecurrentSchedule, Invite, Event, Professional, Topic
from sqlalchemy.orm import object_mapper
from fastapi import status

class GetInvite:
    @handle_errors
    def run (
        db: Session,
        inviteR: Repository[Invite],
        invite_id: str
    ):
        invites = inviteR.getProfInvites(invite_id)
        
        def to_dict(obj):
            result = {}
            for column in object_mapper(obj).columns:
                value = getattr(obj, column.key)
                if isinstance(value, datetime):
                    result[column.key] = value.isoformat()
                else:
                    result[column.key] = value
            return result

        res = []
        for invite, event, username in invites:
            res.append({
                "invite": to_dict(invite),
                "event": to_dict(event),
                "professional_username": username
            })
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=res)