from ..bd.repositories.CategoryRepository import CategoryRepository
from ..services.category_services.GetCategory import GetCategory
from ..services.category_services.DelCategory import DelCategory

from sqlalchemy.orm import Session


class CategoryController:

    def __init__(self, db:Session):
        self.db = db
        self.categoryR = CategoryRepository(db)

    def createCategory(self, category_name:str):
        return CreateCategory.run(
            db= self.db,
            category_name = category_name,
            categoryR = self.categoryR
        )
    
    def getCategory(self):
        return GetCategory.run(
            db = self.db,
            categoryR= self.categoryR
        )
    

    def delCategory(self, category_name:str):
        return DelCategory.run(
            db= self.db,
            category_name = category_name,
            categoryR = self.categoryR
        )
