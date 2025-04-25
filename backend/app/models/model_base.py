from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base

class MODEL(Base):
    __tablename__ = "model"