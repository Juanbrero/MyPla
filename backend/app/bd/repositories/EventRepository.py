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
    
    def getEventsPage (self, page: int, amount: int):
        # Calcular el offset: (página - 1) * cantidad
        offset = (page - 1) * amount
        
        CreatorUser = aliased(User)
        
        smt = (
            select(Event, Invite, User, CreatorUser)
            .join(Invite,  and_(
                Invite.prof_id == Event.prof_id,
                Invite.day_hour == Event.day_hour
            ))
            .join(User, Invite.invite_id == User.user_id)
            .join(CreatorUser, Event.prof_id == CreatorUser.user_id)
            .where(
                Event.day_hour > datetime.now(),
                Event.confirm == True
            )
            .order_by(asc(Event.day_hour))
            .offset(offset)
            .limit(amount)
        )

        return self.session.execute(smt).all()