from app.auth0.authorization_header_elements import get_bearer_token
from app.auth0.custom_exceptions import PermissionDeniedException
from fastapi import Depends
from app.auth0.json_web_token import JsonWebToken
from app.bd.repositories.UserRepository import UserRepository
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.errors import NotFound


def validate_token(token: str = Depends(get_bearer_token)):
    return JsonWebToken(token).validate()


class PermissionsValidator:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(validate_token)):
        token_permissions = token.get("permissions")
        token_permissions_set = set(token_permissions)
        required_permissions_set = set(self.required_permissions)

        if not required_permissions_set.issubset(token_permissions_set):
            raise PermissionDeniedException

class RolesValidator:
    def __init__(self, required_roles: list[str], roles_claim: str = "https://miplasip.publicvm.com/roles"):
        self.required_roles = required_roles
        self.roles_claim = roles_claim

    def __call__(self, token: dict = Depends(validate_token), db: Session = Depends(get_db)):
        auth0_id = token.get("sub")  # Auth0 user ID
        token_roles = token.get(self.roles_claim, [])
        print(token_roles)
        if not isinstance(token_roles, list):
            token_roles = []

        if not set(self.required_roles).intersection(set(token_roles)):
            raise PermissionDeniedException
        
        userR = UserRepository(db)
        user = userR.get_by({
            'auth0_id': auth0_id
        })
        
        if len(user) <= 0:
            raise NotFound("User id not exist")
        
        return {
            "auth0_id": auth0_id,
            "roles": token_roles,
            "user_id": user[0].user_id
        }