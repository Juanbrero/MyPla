from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.bd.schemas import schema_event
from app.bd.repositories.Repository import Repository
from datetime import datetime, timedelta
from app.models import Meeting, SpecificSchedule, RecurrentSchedule, Invite, Event, Professional, Topic
from fastapi import status


class AcceptInvite:
    @handle_errors
    def run(
        db: Session,
        invite_id: str,
        inviteS: schema_event.InviteConfirm,
        inviteR: Repository[Invite],
        eventR: Repository[Event]
    ):
        invite = inviteR.get_by({
            "invite_id": invite_id,
            "prof_id": inviteS.prof_id,
            "day_hour": inviteS.day_hour
        })
        
        if len(invite) <= 0:
            raise NotFound("Invitation is accept or not exist")
        
        if not (invite[0].accept is None):
            raise ValidationError("Invitation answered")
        
        if inviteS.accept == False:
            inviteR.delete({
                "prof_id": inviteS.prof_id,
                "day_hour": inviteS.day_hour
            })
            eventR.delete({
                "day_hour": inviteS.day_hour,
                "prof_id": inviteS.prof_id
            })
            
        inviteR.update({
            "accept": inviteS.accept
        }, {
            "invite_id": invite_id,
            "prof_id": inviteS.prof_id,
            "day_hour": inviteS.day_hour
        })
        
        eventR.update({
            "confirm": True
        }, {
            "prof_id": inviteS.prof_id,
            "day_hour": inviteS.day_hour
        })
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content="Invitation confirm" if inviteS.accept else "Invitation declined")