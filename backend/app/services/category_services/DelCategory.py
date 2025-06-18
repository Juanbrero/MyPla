from app.bd.repositories.Repository import Repository
from app.models import Category
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session

class DelCategory():
    @handle_errors
    def run(
        db: Session,
        category_name: str,
        categoryR: Repository[Category]
    ):
        category = categoryR.get_by({'category_name':category_name})

        if len(category) == 0:
            raise NotFound('Category not found')
        
        deleted = categoryR.delete({'category_name':category_name})

        return JSONResponse(status_code= status.HTTP_200_OK, content='Category deleted')