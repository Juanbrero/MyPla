from app.models import Invite, Event, Professional, User
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
             select(Invite, EventAlias, User.username)
             .join(EventAlias, and_(
                 Invite.day_hour == EventAlias.day_hour,
                 Invite.prof_id == EventAlias.prof_id
             ))
             .join (Professional,
                 Professional.prof_id == Invite.prof_id
             )
             .join(User,
                 User.user_id == Professional.prof_id
             )
             .where(
                and_(
                    Invite.invite_id == invite_id,
                    Invite.accept.is_(None)
                )
             )
             .order_by(asc(Invite.create))
         )


         return self.session.execute(smt).all()