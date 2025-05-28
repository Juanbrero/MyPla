from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import ValidationError as PydanticValidationError
from json.decoder import JSONDecodeError
from app.bd.bd_exceptions import CompleteHour, MinuteError

class ValidationError(Exception):
    'raises a validation error'
class JSONDecodeError(Exception):
    'raises a JSON error in the body of the query'
class MissingData(Exception):
    'raises when data is missing'
class NotFound(Exception):
    'raises when something is not found'

class ErrorHandler():
    error_map = {
        ValidationError: (status.HTTP_400_BAD_REQUEST, "INVALID_ARGUMENT"),
        MissingData: (status.HTTP_400_BAD_REQUEST, "INVALID_ARGUMENT"),
        NotFound: (status.HTTP_404_NOT_FOUND, "NOT_FOUND"),
        PydanticValidationError: (status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR"),
        JSONDecodeError: (status.HTTP_400_BAD_REQUEST, "INVALID_JSON"),
        IntegrityError: (status.HTTP_400_BAD_REQUEST, "DUPLICATE_ENTRY_OR_CONSTRAINT"),
        DataError: (status.HTTP_400_BAD_REQUEST, "DATA_ERROR"),
        ValueError: (status.HTTP_400_BAD_REQUEST, "VALUE_ERROR"),
        SQLAlchemyError: (status.HTTP_500_INTERNAL_SERVER_ERROR, "DATABASE_ERROR"),
        MinuteError: (status.HTTP_406_NOT_ACCEPTABLE, "Minute value not valid"),
        CompleteHour: (status.HTTP_400_BAD_REQUEST, 'Hour is incomplete'),
    }

    @classmethod
    def run(cls, error: Exception) -> JSONResponse:
        status_code, reason = cls.error_map.get(type(error), (status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_ERROR"))
        message = str(error) or "An unexpected error occurred."
        error_type = type(error).__name__

        print(f"{error_type}: {{'status_code': {status_code}, 'message': '{message}'}}")

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "code": status_code,
                    "message": message,
                    "status": reason,
                }
            }
        )

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return ErrorHandler.run(e)
    return wrapper