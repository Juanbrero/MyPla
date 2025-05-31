from pydantic import BaseModel
from typing import Dict
from . import schema_exception, schema_topic_recurrent, schema_topic_specific, schema_specific, schema_reservation


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
    event: list[schema_specific.SpecificCreate] #Cambiar a esquema de event

class ResponseClass(BaseModel):
    """
    Esquema de clases
      -class_: list[schema_reservation.ReservationClassIn]
    """
    class_: list[schema_reservation.ReservationClassIn]  #Cambiar a esquema de clase

class Response(ResponseException, ResponseSpecific, ResponseRecurrent):
    """
    Esquema de respuesta Event, Exception, Specific y Recurrent
      - recurrent: list[schema_topic_recurrent.TopicRecurrentCr1]
      - specific: list[schema_topic_specific.TopicSpecificCr1]
      - exception: list[schema_specific.ExceptionGet]
      NO - event: list[schema_specific.SpecificCreate]
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
      - avaible:  list[schema_topic_specific.TopicSpecificCr1]
      - exception: list[schema_specific.ExceptionCreate]
    """
    avaible: list[schema_topic_specific.TopicSpecificCr1]
    exception: list[schema_exception.ExceptionCreate]
    

   

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