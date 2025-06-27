from pydantic import BaseModel
from datetime import datetime

class Calificate(BaseModel):
    day_hour: datetime
    prof_id: str
    score: int

class Clases(BaseModel):
    prof_id: str
    day_hour: datetime

class GetCalification(BaseModel):
    calificate: list[Clases]
