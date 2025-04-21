from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List

from app.bd.schemas.schema_prof import Profesional, ProfesionalCreate
import app.models as models
from app.bd.cruds import crud_prof


router = APIRouter(prefix="/profesional",tags=["Profesional"])

@router.post("/create/{prof_id}", 
             response_model=Profesional)
def create_prof(prof : ProfesionalCreate, 
                db : Session = Depends(get_db)):
    return crud_prof.create_prof(db, prof)


@router.get("/all", 
            response_model=List[Profesional])
def read_all_prof(db : Session = Depends(get_db)):
    return crud_prof.get_prof(db)



@router.get("/{id_prof}", response_model=Profesional)
def find_prof(id_prof: int, db: Session = Depends(get_db)):
    response = crud_prof.get_id_prof(db,id_prof)        
    return response