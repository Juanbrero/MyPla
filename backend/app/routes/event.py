from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from ..controllers.EventController import EventController
from app.bd.schemas import schema_event
from app.auth0.dependencies import RolesValidator

router = APIRouter(prefix='/api/event')

@router.post('', tags=['Event'], response_model= schema_event.EventBase )
def create_event(eventS: schema_event.EventBase, db:Session = Depends(get_db)): #user_info = Depends(RolesValidator(["Profesional"]))):

    return EventController(db= db).createEvent(prof_id = "a3f6afdf-0239-454e-a184-efdaf41fcc86", eventS = eventS)


@router.get('', tags=['Event'], response_model= schema_event.EventGet )
def get_events(eventS: schema_event.EventGet = Depends(), db:Session = Depends(get_db)):

    return EventController(db= db).getEvents(eventS = eventS)

@router.patch('/invite', tags=['Event'], response_model= schema_event.InviteConfirm)
def accept_event(inviteS: schema_event.InviteConfirm, db:Session = Depends(get_db)): #user_info = Depends(RolesValidator(["Profesional"]))):

    return EventController(db= db).acceptInvite(invite_id = "9bb43560-9d90-403d-933d-bc3ac6d6abbc", inviteS = inviteS)