from app.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from .Repository import Repository

class UserRepository(Repository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def create(self, data):
        return super().create(**data)
    
    def verifyExist (self, email: str, auth0_id: str):
        stm = (
            select(User)
            .where(
                or_(
                    User.auth0_id == auth0_id,
                    User.email == email
                )
            )
        )
        return self.session.execute(stm).scalars().all()