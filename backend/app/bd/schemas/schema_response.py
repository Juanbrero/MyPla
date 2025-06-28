from pydantic import BaseModel
from typing import Dict
from . import schema_exception, schema_topic_recurrent, schema_topic_specific, schema_specific, schema_reservation
from datetime import datetime


class REvent (BaseModel):
    day_hour: datetime
    end: datetime
    topic: str
    title: str

class RInvite(BaseModel):
    host_username: str
    day_hour: datetime
    end: datetime
    topic: str
    title: str

class ResponseInvite(BaseModel):
  guest: list[RInvite]


class ResponseRecurrent(BaseModel):
    """
    Esquema de lista de dias recurrentes
      - recurrent: list[schema_topic_recurrent.TopicRecurrentCr1]
    """
    recurrent: list[schema_topic_recurrent.TopicRecurrentCr1]

class ResponseSpecific(BaseModel):
     """
     Esquema de lista de dias Especificos
      - specific: list[schema_topic_specific.TopicSpecificCr1]
     """
     specific: list[schema_topic_specific.TopicSpecificCr1]

class ResponseException(BaseModel):
    """
    Esquema de dias excepcionales
      - exception: list[schema_exception.ExceptionGet]
    """
    exception: list[schema_exception.ExceptionGetResponse]

class ResponseEvent(BaseModel):
    """
    Esquema de eventos
      - event: list[schema_specific.SpecificCreate]
    """
    my_events: list[REvent] #Cambiar a esquema de event

class ResponseClass(BaseModel):
    """
    Esquema de clases
      -class_: list[schema_reservation.ReservationClassIn]
    """
    class_: list[schema_reservation.ReservationClassIn]  #Cambiar a esquema de clase

class Response(ResponseException, ResponseSpecific, ResponseRecurrent, ResponseEvent, ResponseInvite):
    """
    Esquema de respuesta Event, Exception, Specific y Recurrent
      - recurrent: list[schema_topic_recurrent.TopicRecurrentCr1]
      - specific: list[schema_topic_specific.TopicSpecificCr1]
      - exception: list[schema_specific.ExceptionGet]
      - my_events: list[REvent]
      - guest: list[RInvite]
    """
    pass
    



class ResponseProfessional(ResponseClass, Response):
    """
    Esquema de respuesta a profesional
      -clase: list[schema_specific.Specific]
    """
    pass
    

class ResponseStudent(BaseModel):
    """
    Esquema de respuesta a alumno
      - available:  list[schema_topic_specific.TopicSpecificCr1]
      - reserv: list[schema_specific.ExceptionCreate]
    """
    available: list[schema_topic_specific.TopicSpecificCr1]
    reserv: list[schema_exception.ExceptionCreate]
    

   

"""recurrent: [{
  start: Time,
  end: time,
  week_day: integer o enum (dia recurrente),
  topics: string[]
}]
specific: [{
  date: Date
  start: Time,
  end: time,
  topics: string[]
}]
exception: [{
  date: Date
  start: Time,
  end: time,
}]
class: [{
  start: Time,
  date: Date,
  topic: string
}]
event: [{
  start: Time,
  end: Time,
  date: Date,
  id_evento: string // no hay id pero es pa consultar digamo
}]
"""