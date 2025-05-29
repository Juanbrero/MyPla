from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from .schema_prof import ProfessionalID


class ExceptionBase(BaseModel):
    """
        - day
        - start
        - end
    """
    day: date
    start: time
    end: time

class ExceptionCreate(ExceptionBase, ProfessionalID):
    """
       - day
       - start
       - end
       - prof_id
    """
    pass

class ExceptionDel(BaseModel):
    """
        - day
        - start
    """
    day: date
    start: time

class ExceptionDelete(ExceptionDel, ProfessionalID):
    """
        - day
        - start
        - prof_id
    """
    pass

class ExceptionGetResponse(ExceptionBase):
    """
    ORM
        - day
        - start
        - end
    """

    class Config:
        orm_mode=True

class ExceptionUpInfo(BaseModel):
    """
        - day
        - end
    """
    day: date
    start: time
    Nday: Optional[date]
    Nstart: Optional[time]
    Nend: Optional[time]

class ExceptionUpdate(ExceptionUpInfo, ProfessionalID):
    """
        - day
        - end
        - Nday
        - Nend
        - Nstart
    """
    pass

