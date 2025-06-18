from app.bd.repositories.Repository import Repository
from app.models import Category
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session

class CreateCategory():
    @handle_errors
    def run(
        db:Session,
        category_name: str,
        categoryR: Repository[Category]
    ):
        category_name = category_name.upper()

        category = categoryR.get_by({'category_name': category_name})

        if len(category) > 0:
            raise ValueError('Category exist')
        
        category = categoryR.create({'category_name':category_name})
        
        db.commit()

        return JSONResponse(status_code= status.HTTP_201_CREATED, content='Category created')