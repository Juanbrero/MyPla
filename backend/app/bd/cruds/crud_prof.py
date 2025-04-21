from sqlalchemy.orm import Session
from app.bd.schemas import schema_prof
import app.models as models


def get_prof(db: Session):
    return db.query(models.Profesional).all()

def create_prof(db: Session, prof_c: schema_prof.ProfesionalCreate):
    try:
        db_prof = models.Profesional(**prof_c.dict())
        db.add(db_prof)
        db.commit()
        db.refresh(db_prof)
    except:
        db_prof = {'Error':'on create_pof'}
    return db_prof

def get_id_prof(db:Session, id_prof: int):
    try:
        response = db.query(models.Profesional).get(id_prof)
        if response is None:
            response = {"id":-1, "score":-1}
    except:
        response = {'Error':'On get_id_prof'}
    return response