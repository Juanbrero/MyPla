from app.bd.repositories.Repository import Repository
from app.models import Category
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session

class GetCategory():
    @handle_errors
    def run(
        db: Session,
        categoryR: Repository[Category]
    ):
        all_categorys = categoryR.get_all()

        response = [category.category_name for category in all_categorys]

        return JSONResponse(status_code= status.HTTP_200_OK, content= response)

