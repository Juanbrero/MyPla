from ..bd.repositories.MeetingRepository import MeetingRepository
from ..bd.repositories.ProfessionalRepository import ProfessionalRepository
from ..bd.repositories.EventRepository import EventRepository
from ..bd.repositories.InviteRepository import InviteRepository
from ..bd.repositories.TopicRepository import TopicRepository
from ..services.event_services.CreateEvent import CreateEvent
from ..services.event_services.AcceptInvite import AcceptInvite
from ..services.event_services.GetEvents import GetEvents
from ..services.event_services.GetInvite import GetInvite
from sqlalchemy.orm import Session
from app.bd.schemas import schema_event


class EventController():

    def __init__ (self, db: Session):
        self.db = db
        self.meetingR = MeetingRepository(db)
        self.eventR = EventRepository(db)
        self.inviteR = InviteRepository(db)
        self.professionalR = ProfessionalRepository(db)
        self.topicR = TopicRepository(db)


    def createEvent(self, prof_id: str, eventS: schema_event):
        return CreateEvent.run(
            db = self.db, 
            eventS = eventS,
            prof_id = prof_id, 
            meetingR = self.meetingR,
            eventR = self.eventR,
            inviteR = self.inviteR,
            professionalR = self.professionalR,
            topicR = self.topicR
        )
        
    def getEvents (self, eventS: schema_event.EventGet):
        return GetEvents.run(
            db=self.db,
            eventS=eventS,
            eventR=self.eventR
        )
    
    def acceptInvite (self, invite_id: str, inviteS: schema_event.InviteConfirm):
        return AcceptInvite.run(
            db=self.db,
            invite_id = invite_id,
            inviteS=inviteS,
            inviteR=self.inviteR,
            eventR=self.eventR
        )

    def getInvite (self, invite_id):
        return GetInvite.run(
            db = self.db,
            inviteR = self.inviteR,
            invite_id = invite_id
        )