from app.utils.errors import handle_errors, ValidationError
from app.bd.schemas import schema_users
from sqlalchemy.orm import Session
from app.bd.repositories.Repository import Repository
from app.models import User, Student, Professional
from fastapi.responses import JSONResponse
from fastapi import status

class CreateUser:
    @handle_errors
    def run (
        db: Session,
        userS: schema_users.UsersCreate,
        userR: Repository[User],
        studentR: Repository[Student],
        professionalR: Repository[Professional]
    ):
        if userS.role != 'Profesional' and userS.role != 'Alumno':
            raise ValidationError("Invalid type user")

        user = userR.verifyExist(
            email = userS.email,
            auth0_id = userS.auth0_id
        )
        
        if (len(user) > 0):
            raise ValidationError("User exist")
        
        userData = {
            "auth0_id": userS.auth0_id,
            "email": userS.email,
            "username": userS.username,
        }
        
        
        newUser = userR.create(userData)
        db.flush()
        
        if userS.role == 'Profesional':
            professionalR.create({
                "prof_id": newUser.user_id,
                "cvu": userS.cvu_profesional,
                "link_acceso": userS.link_acceso
            }) 
        else:
            studentR.create({
                "student_id": newUser.user_id,
                "cvu": userS.cvu_alumno
            })
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content="User created")
        