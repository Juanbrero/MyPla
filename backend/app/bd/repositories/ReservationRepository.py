from app.models import Reservation
from sqlalchemy.orm import Session
from .Repository import Repository

class ReservationRepository(Repository[Reservation]):
    def __init__(self, session: Session):
        super().__init__(Reservation, session)

    def create(self, data):
        return super().create(**data)