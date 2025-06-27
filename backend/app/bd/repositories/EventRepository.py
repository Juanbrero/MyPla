from app.models import Event, Professional, Invite, User, Meeting
from sqlalchemy.orm import Session, aliased
from sqlalchemy import asc, select, and_, func
from .Repository import Repository
from datetime import datetime
from math import ceil

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
            select(EventAlias, Invite, User, CreatorUser, Meeting.topic_name)
            .outerjoin(Invite, and_(
                Invite.prof_id == EventAlias.prof_id,
                Invite.day_hour == EventAlias.day_hour
            ))
            .outerjoin(User, Invite.invite_id == User.user_id)
            .join(CreatorUser, EventAlias.prof_id == CreatorUser.user_id)
            .join(Meeting, and_(
                Meeting.prof_id == EventAlias.prof_id,
                Meeting.day_hour == EventAlias.day_hour
            ))
            .order_by(asc(EventAlias.day_hour))
        )
    
        return self.session.execute(smt).all()
    
    def getTotalEventPages(self, amount: int) -> int:
        total_events_query = (
            select(func.count())
            .select_from(Event)
            .where(
                Event.day_hour > datetime.now(),
                Event.confirm == True
            )
        )
    
        total_events = self.session.execute(total_events_query).scalar()
        total_pages = ceil(total_events / amount) if amount > 0 else 0
    
        return total_pages