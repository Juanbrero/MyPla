from pydantic import BaseModel
from typing import Dict
from . import schema_specific, schema_topic_recurrent, schema_topic_specific


class ResponseRecurrent(BaseModel):
    recurrent: list[schema_topic_recurrent.TopicRecurrentCr1]

class ResponseSpecific(BaseModel):
     specific: list[schema_topic_specific.TopicSpecificCr1]

class ResponseException(BaseModel):
    exception: list[schema_specific.ExceptionGet]

class ResponseEvent(BaseModel):
    event: list[schema_specific.SpecificCreate] #Cambiar a esquema de event

class ResponseClass(BaseModel):
    clase: list[schema_specific.Specific]  #Cambiar a esquema de clase

class Response(ResponseEvent, ResponseException, ResponseSpecific, ResponseRecurrent):
    pass
    """
    recurrent: list[schema_topic_recurrent.TopicRecurrentCr1]
    specific: list[schema_topic_specific.TopicSpecificCr1]
    exception: list[schema_specific.ExceptionGet]
    event: list[schema_specific.SpecificCreate] """



class ResponseProfessional(ResponseClass, Response):
    pass
    #clase: list[schema_specific.Specific]

class ResponseAlumno(Response):
    pass
    

   

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