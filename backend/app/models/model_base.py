from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, ForeignKeyConstraint 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from typing import List
from datetime import datetime

class MODEL(Base):
    __tablename__ = "model"