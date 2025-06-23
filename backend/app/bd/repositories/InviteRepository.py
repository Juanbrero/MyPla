from app.models import Invite
from sqlalchemy.orm import Session
from .Repository import Repository

class InviteRepository(Repository[Invite]):
    def __init__(self, session: Session):
        super().__init__(Invite, session)

    def create(self, data):
        return super().create(**data)