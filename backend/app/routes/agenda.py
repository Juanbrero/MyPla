from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union
from pydantic import BaseModel
from datetime import date

from app.bd.schemas import schema_topic_recurrent,  schema_response, schema_topic_specific, schema_specific
from app.bd.cruds import crud_topic_recurrent, crud_topic_specific, crud_specific
from app.bd.bd_utils import Errors


router = APIRouter(prefix="/prof/{prof_id}/agenda")


#SPECIFIC

#Crea el dia disponible especifico, con los topicos
@router.post('/create/spec',tags=["Specific"], response_model=Union[schema_topic_specific.TopicSpecificIn, Errors])
def create_specific_day(prof_id:str, specific:schema_topic_specific.TopicSpecificCr1, db:Session = Depends(get_db)):
    topicS = schema_topic_specific.TopicSpecificIn(**specific.dict(), prof_id= prof_id, isCanceling= False)
    return crud_topic_specific.create2(topicS, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/get/spec',tags=["Specific"],response_model=Union[schema_response.ResponseSpecific, List[schema_topic_specific.TopicSpecificCr1], Errors])
def get_specific(prof_id:str,  db:Session = Depends(get_db)):
    topicS = schema_topic_specific.TopicSpecificID( prof_id= prof_id)
    return {'specific': crud_topic_specific.get2(topicS, db)}

#crear excepciones, iscanceling= True
@router.post('/create/exception', tags=["Specific"], response_model=Union[schema_specific.Specific, Errors])
def create_exception(prof_id:str, excep:schema_specific.Specific, db: Session = Depends(get_db)):
    excepcion = schema_specific.SpecificIsCancel(**excep.dict(), prof_id= prof_id, isCanceling= True)
    return crud_specific.create_exception(db, excepcion)

@router.get('/get/exception', tags=["Specific"], response_model=Union[schema_response.ResponseException, Errors])
def get_exception(prof_id:str, db: Session = Depends(get_db)):
    excepcion = schema_specific.SpecificID(prof_id= prof_id)
    return {'exception': crud_specific.get_exception(db, excepcion)}


#RECURRENT
#Crea el recurrent, con los topicos
@router.post('/create/recurrent',tags=["Recurrent"], response_model=Union[schema_topic_recurrent.TopicRecurrentIn, Errors])
def create_recurrent(prof_id:str, recurrent:schema_topic_recurrent.TopicRecurrentCr1, db:Session = Depends(get_db)):
    topicr = schema_topic_recurrent.TopicRecurrentIn(**recurrent.dict(), prof_id= prof_id)
    return crud_topic_recurrent.create2(topicr, db)

#Recupera los datos del profesioanl especificado
#Retorna un diccionario con los datos recuperados
@router.get('/get/recurrent',tags=["Recurrent"],response_model=Union[schema_response.ResponseRecurrent, List[schema_topic_recurrent.TopicRecurrentCr1], Errors])
def get_recurrent(prof_id:str,  db:Session = Depends(get_db)):
    topicr = schema_topic_recurrent.TopicRecurrentID( prof_id=prof_id)
    return {'recurrent': crud_topic_recurrent.get2(topicr, db)}


## Codigos individuales de ingreso ver si seran utiles
#Specific
"""#trae todos los dias sin filtro 
@router.get("/list/specificday",
            response_model=List[schema_specific.SpecificSchema],
            tags=["Specific"])
async def get_all_dias(db: Session = Depends(get_db)):
    return crud_specific.get_all_specific(db)

#Crea un dia especifico para un profesional
@router.post("/create/specificday", 
             response_model=Union[schema_specific.Specific, Errors], 
             tags=["Specific"])
async def create_dia(dia: schema_specific.SpecificCreate,
                prof_id: str, 
                db: Session= Depends(get_db)):
    specific = schema_specific.SpecificSchema(**dia.dict(), prof_id=prof_id)
    return crud_specific.create_specific(db, specific)


#Recupera todos los horarios de un profesional especificado
@router.get("/all/specific",
            response_model=List[schema_specific.Specific],
            tags=["Specific"])
async def get_day(prof_id:str, db: Session = Depends(get_db)):
    specific = schema_specific.SpecificSchemaID(prof_id=prof_id)
    return crud_specific.get_day(db, specific)


#@router.delete("/delete/specific",               response_model=Union[schema_specific.SpecificSchema, Errors],               tags=["Specific"])
async def del_day(prof_id:str, delete:schema_specific.SpecificDel, db:Session = Depends(get_db)):
    delete = schema_specific.SpecificSchema(**delete.dict(), prof_id=prof_id)
    return crud_specific.del_day(db, delete)
"""
#Recurrent
"""@router.get("/list/recurrent", 
            response_model=List[schema_recurrent.Recurrent],
              tags=["Recurrent"])
async def get_dias(prof_id:str, db: Session = Depends(get_db)):
    recurrent = schema_recurrent.RecurrentSchemaID(prof_id=prof_id)
    return crud_recurrent.get_all_recurrent(db, recurrent)

#Creaba el recurrent y operaba sobre el
#@router.post("/create/recurent",              response_model=Union[schema_recurrent.Recurrent, Errors],              tags=["Recurrent"])
async def create_recurrent(dia: schema_recurrent.RecurrentCreate, prof_id: str, db: Session = Depends(get_db)):
    recurrent = schema_recurrent.RecurrentSchema(**dia.dict(), prof_id=prof_id)
    return crud_recurrent.create_recurrent(db, recurrent)

#@router.get("/day/{week_day}",            response_model=Union[List[schema_recurrent.Recurrent], Errors],            tags=["Recurrent"])
async def get_day(prof_id:str, week_day:str, db: Session = Depends(get_db)):
    recurrent = schema_recurrent.RecurrentSchema(week_day=week_day, prof_id=prof_id)
    return crud_recurrent.get_day(db, recurrent)

#@router.delete("/delete/recurrent",               response_model=Union[schema_recurrent.RecurrentSchema, Errors],               tags=["Recurrent"])
async def del_day(prof_id:str, delete:schema_recurrent.RecurrentDel, db:Session = Depends(get_db)):
    delete = schema_recurrent.RecurrentSchema(**delete.dict(), prof_id=prof_id)
    return crud_recurrent.del_day(db, delete)


##
#Solo crea la relacion topic recurent
#@router.post('/add/topic', response_model=Union[schema_topic_recurrent.TopicRecurrentCreate,Errors], tags=["TOPICR"])
def add_topic_recurrent(prof_id:str, topico:schema_topic_recurrent.TopicRecurrentBase, db:Session = Depends(get_db)):
    topicr = schema_topic_recurrent.TopicRecurrentCreate(**topico.dict(), prof_id=prof_id)
    return crud_topic_recurrent.create(topicr,db)

#@router.get('/get/topics',response_model=Union[List[schema_topic_recurrent.TopicRecurrent], Errors],tags=["TOPICR"])
def get_topic_recurrent(prof_id:str, week:int, start:time, db:Session = Depends(get_db)):
    topicr = schema_topic_recurrent.TopicRecurrentSchema(prof_id=prof_id, week_day=week, start=start)
    return crud_topic_recurrent.get(topicr,db)
##
"""