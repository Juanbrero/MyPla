from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List, Union

from app.bd.schemas import schema_prof
import app.models as models
from app.bd.cruds import crud_prof
from app.bd.bd_utils import Errors, Info

router = APIRouter(prefix="/professionals",tags=["Professionals"])


@router.get("", 
            response_model=List[schema_prof.Professional])
async def get_all_prof(db : Session = Depends(get_db)):
    """
    Retorna todos los profesionales
    Args:
        db: Session
    Return
        [Professionales]

    """
    return crud_prof.get_prof(db)


@router.get("/{prof_id}", response_model=Union[schema_prof.Professional, Errors])
async def find_prof(prof_id: str, db: Session = Depends(get_db)):
    """
    Retorna un profesional
    Args:
        prof_id: str
        db: Session
    Return
        Professional
        Errors

    """
    response = crud_prof.get_prof_id(db, prof_id)       
    return response


@router.delete("/{prof_id}",response_model=Union[Info, Errors])
def del_user(prof_id:str, db:Session = Depends(get_db)):
    """
    Eliminar un profesional

    Args:
        prof_id: str
        db: Session
    Returns:
        Info
        Errors
    """
    return crud_prof.del_prof(db, prof_id)


#Para Desarrollo
@router.post("", 
             response_model=Union[Info, Errors])
async def create_prof(prof : schema_prof.ProfessionalID, 
                db : Session = Depends(get_db)):
    """
    Funcion de desarrollo para crear un profesional

    Args:
        prof_id: str
        db: Session

    Return:
        Info
        Errors
    """
    return crud_prof.create_prof(db, prof.prof_id)

@router.put("/{prof_id}",response_model=Union[schema_prof.Professional, Errors])
def update_score(prof_id:str, score:schema_prof.ProfessionalScore, db:Session = Depends(get_db)):
    """
    Funcion de desarrollo para definir score

    Args:
        prof_id: str
        score: schema_prof.ProfessionalScore
            - score: float
        db: Session
    Return:
        schema_prof.Professional
            - prof_id: str
            - scores: float
        Errors
    """
    prof = schema_prof.Professional(prof_id=prof_id, score= score.score)
    return crud_prof.update_score(db, prof)

