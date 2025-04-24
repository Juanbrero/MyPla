from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union

from app.bd.schemas.schema_prof import Profesional, ProfesionalCreate
import app.models as models
from app.bd.cruds import crud_prof
from app.bd.bd_utils import Errors, Info

router = APIRouter(prefix="/profesional",tags=["Profesional"])

@router.post("/create/", 
             response_model=Union[Profesional,Errors])
async def create_prof(prof : ProfesionalCreate, 
                db : Session = Depends(get_db)):
    return crud_prof.create_prof(db, prof)


@router.get("/all", 
            response_model=List[Profesional])
async def read_all_prof(db : Session = Depends(get_db)):
    return crud_prof.get_prof(db)



@router.get("/{id_prof}", response_model=Union[Profesional, Errors])
async def find_prof(id_prof: int, db: Session = Depends(get_db)):
    response = crud_prof.get_id_prof(db, id_prof)        
    return response

@router.put("/{id_prof}/score",response_model=Union[Profesional, Errors])
def update_score(id_prof:int, score:float, db:Session = Depends(get_db)):
    return crud_prof.update_score(db, id_prof, score)

@router.delete("/{id_prof}/delete",response_model=Union[Info, Errors])
def del_user(id_prof:int, db:Session = Depends(get_db)):
    return crud_prof.del_prof(db, id_prof)