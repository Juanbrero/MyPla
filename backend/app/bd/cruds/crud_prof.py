from sqlalchemy.orm import Session
from app.bd.schemas import schema_prof
from app.models.Profesional import Profesional


def get_prof(db: Session):
    return db.query(Profesional).all()

def create_prof(db: Session, prof_c: schema_prof.ProfesionalCreate):
    try:
        db_prof = Profesional(**prof_c.dict())
        db.add(db_prof)
        db.commit()
        db.refresh(db_prof) #<- Fallaria aca, no antes
    except:
        db_prof = {'error':'on create_pof'}
    return db_prof

def get_id_prof(db:Session, id_prof: int):
    try:
        response = db.query(Profesional).get(id_prof)
        if response is None: #<- Se define la falla
            response = {"error":"id no existente"}
    except:
        response = {'error':'On get_id_prof'}
    return response

def update_score(db:Session, id_prof:int, score:float):
    if score in range (0,5):
        db.query(Profesional).filter(Profesional.user_id == id_prof).update({"score": score})
        db.commit()
        return db.query(Profesional).get(id_prof)
    else:
        return {'error':'Value out of range (0-5)'}
    
def del_prof(db:Session, id_prof:int):
    try:
        smt = db.get(Profesional, id_prof)
        db.delete(smt) 
        #db.query(Profesional).filter(Profesional.user_id == id_prof).delete() no es afectado por el try
        db.commit()
        return {'INFO':f'Delete of Profesioanl {id_prof}'}
    except:
        return {"error":'error'}