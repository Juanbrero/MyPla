from dataclasses import dataclass

import jwt
from app.auth0.config import settings
from app.auth0.custom_exceptions import BadCredentialsException, UnableCredentialsException


@dataclass
class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    jwt_access_token: str
    auth0_issuer_url: str = f"https://{settings.auth0_domain}/"
    auth0_audience: str = settings.auth0_audience
    algorithm: str = "RS256"
    jwks_uri: str = f"{auth0_issuer_url}.well-known/jwks.json"

    def validate(self):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
                self.jwt_access_token
            ).key
            print("jwt_access_token: ", self.jwt_access_token)
            print("jwt_signing_key: ", jwt_signing_key)
            print("algorithms: ", self.algorithm)
            print("audience: ", self.auth0_audience)
            print("issuer: ", self.auth0_issuer_url)
            payload = jwt.decode(
                self.jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
            )
            print("FALLO LA VAINA DE TOKEN")
        except jwt.exceptions.PyJWKClientError:
            raise UnableCredentialsException
        except jwt.exceptions.InvalidTokenError:
            raise BadCredentialsException
        return payload
