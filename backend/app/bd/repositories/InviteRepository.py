from app.models import Invite, Event
from sqlalchemy import select, cast, Time, func, and_, asc
from sqlalchemy.orm import Session, aliased
from .Repository import Repository

class InviteRepository(Repository[Invite]):
    def __init__(self, session: Session):
        super().__init__(Invite, session)

    def create(self, data):
        return super().create(**data)
    
    def getProfInvites(self, invite_id: str):
         EventAlias = aliased(Event)

         smt = (
             select(Invite, EventAlias)
             .join(EventAlias, and_(
                 Invite.day_hour == EventAlias.day_hour,
                 Invite.prof_id == EventAlias.prof_id
             ))
             .where(Invite.invite_id == invite_id)
             .order_by(asc(Invite.create))
         )


         return self.session.execute(smt).all()