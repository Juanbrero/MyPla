from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controllers.CategoryController import CategoryController
from app.auth0.dependencies import RolesValidator



router = APIRouter(prefix="/api/category", tags=["Category"])

@router.get("")
def get_category(db:Session =Depends(get_db)):
    """
       - Get all category
            - Return:
                - list [str]
    """
    return CategoryController(db= db).getCategory()

@router.delete("")
def del_category(category_name:str, db:Session = Depends(get_db)):
    """
    - Delete category
        - param category_name
    """
    return CategoryController(db= db).delCategory(category_name= category_name)

 