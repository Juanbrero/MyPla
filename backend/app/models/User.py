from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    professional: Mapped['Professional'] = relationship(back_populates='user', cascade='all, delete-orphan')
    #student: Mapped['Student'] = relationship(back_populates='user', cascade='all, delete-orphan')

