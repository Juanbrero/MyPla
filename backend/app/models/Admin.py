from sqlalchemy import Column, Integer, String, text, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
'''
from sqlalchemy import ForeignKey
'''
from app.config.database import Base

class Admin(Base):
    __tablename__  = "professional"

    admin_id: Mapped[str]  = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"),
                                    primary_key=True,
                                    index=True)

