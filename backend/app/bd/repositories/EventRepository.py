from app.models import Event, Professional, Invite, User, Meeting
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
        offset = (page - 1) * amount
        CreatorUser = aliased(User)
    
        # event_subq = (
        # select(Event)
        #     .where(
        #         Event.day_hour > datetime.now(),
        #         Event.confirm == True
        #     )
        #     .order_by(asc(Event.day_hour))
        #     .offset(offset)
        #     .limit(amount)
        #     .subquery()
        # )
    
        # EventAlias = aliased(Event, event_subq)
    
        # smt = (
        #     select(EventAlias, Invite, User, CreatorUser, Meeting.topic_name)
        #     .join(Invite, and_(
        #         Invite.prof_id == EventAlias.prof_id,
        #         Invite.day_hour == EventAlias.day_hour
        #     ))
        #     .join(User, Invite.invite_id == User.user_id)
        #     .join(CreatorUser, EventAlias.prof_id == CreatorUser.user_id)
        #     .join(Meeting, and_(Meeting.prof_id == CreatorUser.user_id,
        #                         Meeting.day_hour == EventAlias.day_hour)
        #                         )
        #     .order_by(asc(EventAlias.day_hour))
        # )

        # return self.session.execute(smt).all()

        # Paso 1: obtener eventos paginados
        events_stmt = (
            select(Event)
            .where(
                Event.day_hour > datetime.now(),
                Event.confirm == True
            )
            .order_by(asc(Event.day_hour))
            .offset(offset)
            .limit(amount)
        )

        events = self.session.execute(events_stmt).scalars().all()

        if not events:
            return []

        # Paso 2: traer info relacionada para esos eventos
        results = []
        for ev in events:
            smt = (
                select(Event, Invite, User, CreatorUser, Meeting.topic_name)
                .select_from(Event)
                .join(Invite, and_(
                    Invite.prof_id == Event.prof_id,
                    Invite.day_hour == Event.day_hour
                ))
                .join(User, Invite.invite_id == User.user_id)
                .join(CreatorUser, Event.prof_id == CreatorUser.user_id)
                .join(Meeting, and_(
                    Meeting.prof_id == Event.prof_id,
                    Meeting.day_hour == Event.day_hour
                ))
                .where(
                    Event.prof_id == ev.prof_id,
                    Event.day_hour == ev.day_hour
                )
            )

            related_data = self.session.execute(smt).all()
            results.extend(related_data)

        return results