from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    auth0_id: Mapped[str] = mapped_column(
        String, 
        unique=True, 
        nullable=False, 
        index=True
    )
    username: Mapped[str] = mapped_column(
        String, 
        nullable=False, 
    )
    name: Mapped[str] = mapped_column(nullable=False)

    #professional: Mapped['Professional'] = relationship(back_populates='user', cascade='all, delete-orphan')
    #student: Mapped['Student'] = relationship(back_populates='user', cascade='all, delete-orphan')

