from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union

from app.bd.schemas import schema_prof
import app.models as models
from app.bd.cruds import crud_prof
from app.bd.bd_utils import Errors, Info

router = APIRouter(prefix="/professional",tags=["Professional"])



@router.get("/all", 
            response_model=List[schema_prof.Professional])
async def read_all_prof(db : Session = Depends(get_db)):
    return crud_prof.get_prof(db)


@router.get("/{prof_id}", response_model=Union[schema_prof.Professional, Errors])
async def find_prof(prof_id: str, db: Session = Depends(get_db)):
    response = crud_prof.get_prof_id(db, prof_id)  
    ic(f'GET PROF')      
    return response


@router.delete("/{prof_id}/delete",response_model=Union[Info, Errors])
def del_user(prof_id:str, db:Session = Depends(get_db)):
    return crud_prof.del_prof(db, prof_id)


#Para Desarrollo
@router.post("/{prof_id}/create/", 
             response_model=Union[Info, Errors])
async def create_prof(prof_id : str, 
                db : Session = Depends(get_db)):
    return crud_prof.create_prof(db, prof_id)

@router.put("/{prof_id}/score",response_model=Union[schema_prof.Professional, Errors])
def update_score(prof_id:str, score:schema_prof.ProfessionalScore, db:Session = Depends(get_db)):
    prof = schema_prof.Professional(prof_id=prof_id, score= score.score)
    return crud_prof.update_score(db, prof)

