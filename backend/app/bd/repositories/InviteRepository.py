from app.models import Invite, Event, User, Professional, Meeting
from sqlalchemy import select, cast, Time, func, and_, asc
from sqlalchemy.orm import Session, aliased
from .Repository import Repository
from datetime import datetime

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
    
    def getProfTrue(self, invite_id:str):
        """
          - Retorna todas las invitaciones que el profesional acepto
          - Utilizado para mostrar disponibilidad al ESTUDIANTE  
          - Retorna:
            - Todos los datos de la invitacion
            - la duracion del evento
        """
        EventAlias = aliased(Event)

        smt = (
             select(Invite, EventAlias.duration)
             .join(EventAlias, and_(
                 Invite.day_hour == EventAlias.day_hour,
                 Invite.prof_id == EventAlias.prof_id
             ))
             .where(Invite.invite_id == invite_id,
                    Invite.accept == True)
             .order_by(asc(Invite.day_hour))
         )
        
        return self.session.execute(smt).all()
    
    def getProfInvitation(self, invite_id:str):
        """
            - Recupera todas las invitaciones que el profesional acepto
            - Utilizado para mostrar en el calendario al PROFESIONAL
            - Retorna:
                - todos los datos de Invitacion
                - titulo del evento
                - nombre del anfitrion
                - topico del evento
        
        """
        EventAlias = aliased(Event)

        smt = (
             select(Invite, EventAlias, User.username, Meeting.topic_name)
             .join(EventAlias, and_(
                 Invite.day_hour == EventAlias.day_hour,
                 Invite.prof_id == EventAlias.prof_id
             ))
             .join(User, 
                   Invite.prof_id == User.user_id)
             .join(Meeting, and_(
                 Meeting.prof_id == Invite.prof_id,
                 Meeting.day_hour == Invite.day_hour
             ))
             .where(Invite.invite_id == invite_id,
                    Invite.accept == True)
             .order_by(asc(Invite.day_hour))
         )
        
        return self.session.execute(smt).all()

    def getInvitate(self, prof_id:str, day_hour:datetime):
        stm = (
            select(User.username)
            .select_from(Invite)
            .join(User, Invite.invite_id == User.user_id)
            .where(Invite.prof_id == prof_id,
                   Invite.day_hour == day_hour)
        )
        return self.session.execute(stm).scalars().all()
