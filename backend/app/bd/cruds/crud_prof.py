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


def get_prof_id(db:Session, professional: schema_prof.ProfessionalID):
    """
    Retorna un profesional
    Args:
        db (Session)
        professional (schema_prof.ProfessionalID)
            - prof_id: str
    Return:
        {prof_id:, score:}
        {'error':}
    """
    try:
        smt = select(Professional).where(Professional.prof_id == professional)
        response = db.scalars(smt).first()
        if response is None: #<- Se define la falla
            response = {"error": "id no existente"}
    except:
        response = {'error':'On get_id_prof'}
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
    try:
        smt = delete(Professional).where(Professional.prof_id == id_prof)
        response = db.execute(smt)
        #db.query(Professional).filter(Professional.prof_id == id_prof).delete() no es afectado por el try
        if response.rowcount > 0:
            db.commit()
            return {'info':f'Delete of Profesional {id_prof}'}
        else:
            raise
    except:
        return {"error":f'On delete Professional {id_prof}'}
    

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
        db.query(Professional).filter(Professional.prof_id == prof.prof_id).update({"score": prof.score})
        db.commit()
        return db.query(Professional).get(prof.prof_id)
    else:
        return {'error':'Value out of range (0-5)'}
    
