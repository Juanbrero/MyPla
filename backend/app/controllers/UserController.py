from ..services.user_services.CreateUser import CreateUser
from app.bd.schemas import schema_users
from ..bd.repositories.UserRepository import UserRepository
from ..bd.repositories.ProfessionalRepository import ProfessionalRepository
from ..bd.repositories.StudentRepository import StudentRepository

from sqlalchemy.orm import Session

class UserController:
    def __init__ (self, db: Session):
        self.db = db
        self.userR = UserRepository(db)
        self.studentR = StudentRepository(db)
        self.professionalR = ProfessionalRepository(db)
    
    def createUser(self, userS: schema_users.UsersCreate):
        return CreateUser.run(
            db = self.db,
            userS = userS,
            userR = self.userR,
            studentR = self.studentR,
            professionalR = self.professionalR
        )