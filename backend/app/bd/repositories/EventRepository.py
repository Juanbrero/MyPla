from app.models import Event, Professional, Invite, User
from sqlalchemy.orm import Session, aliased
from sqlalchemy import asc, select, and_
from .Repository import Repository
from datetime import datetime

class EventRepository(Repository[Event]):
    def __init__(self, session: Session):
        super().__init__(Event, session)

    def create(self, data):
        return super().create(**data)
    
    
    def getEventsPage(self, page: int, amount: int):
        offset = (page - 1) * amount
        CreatorUser = aliased(User)
    
        event_subq = (
            select(Event)
            .where(
                Event.day_hour > datetime.now(),
                Event.confirm == True
            )
            .order_by(asc(Event.day_hour))
            .offset(offset)
            .limit(amount)
            .subquery()
        )
    
        EventAlias = aliased(Event, event_subq)
    
        smt = (
            select(EventAlias, Invite, User, CreatorUser)
            .outerjoin(Invite, and_(
                Invite.prof_id == EventAlias.prof_id,
                Invite.day_hour == EventAlias.day_hour
            ))
            .outerjoin(User, Invite.invite_id == User.user_id)
            .join(CreatorUser, EventAlias.prof_id == CreatorUser.user_id)
            .order_by(asc(EventAlias.day_hour))
        )
    
        return self.session.execute(smt).all()