from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from app.config.database import Base

class Event(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    fecha = Column(TIMESTAMP, nullable=False)