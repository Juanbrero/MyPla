from sqlalchemy.orm import Session
from app.bd.schemas import schema_prof
from app.models.Professional import Professional
from sqlalchemy import select, insert, delete


def get_prof(db: Session):
    """
    Retorna todos los profesionales
    Args:
        db (Session)
    Return:
        [{prof_id:, score:}]
    """
    return db.query(Professional).all()


def get_prof_id(db:Session, prof_id: schema_prof.ProfessionalID):
    """
    Retorna un profesional
    Args:
        db (Session)
        professional (schema_prof.ProfessionalID)
            - prof_id: str
    Return:
        {prof_id:, score:}
        None
    """
    response = db.query(Professional).filter(Professional.prof_id == prof_id).first()
    return response


def del_prof(db:Session, id_prof:schema_prof.ProfessionalID):
    """
    elimina un profesional
    Args:
        db (Session)
        id_prof: schema_prof.ProfessionalID
            - prof_id:str
    Return:
        {'info':}
        {'error':}
    """
    response = db.query(Professional).filter(Professional.prof_id == id_prof).first()
    if not response is None:
        db.delete(response)
        db.commit()
        return True
    else:
        return False
    

#TEST, se hace por back
def create_prof(db: Session, prof_c: schema_prof.ProfessionalID):
    """
    Funcion de pruebas para definir un profesional

    Args:
        db: Session
        prof_c: schema_prof.ProfessionalID
            - prof_id: str
    Return:
        {'info':}
        {'error':}
    """
    try:
        smt = insert(Professional).values(prof_id = prof_c)
        response = db.execute(smt)
        db.commit()
        #db.refresh(prof_c) #<- Fallaria aca, no antes
        return {'info':f'Insert existos {prof_c}'}
    except:
        return {'error':f'ID {prof_c} existente'}



def update_score(db:Session, prof:schema_prof.Professional):
    """
    Funcion que define el score como el valor entregados

    Args:
        db: Session
        prof: schema_prof.Professional
            - prof_id:str
            - score: int [0-5]
    Return:
        {prof_id:, score:}
        {'error':}
    """
    if prof.score in range (0, 6):
        prof_update = db.query(Professional).filter(Professional.prof_id == prof.prof_id).first()
        if prof_update:
            prof_update.score = prof.score
            db.commit()
        return prof_update
    else:
        return {'error':'Value out of range (0-5)'}
    
