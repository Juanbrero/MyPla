from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_topic
from sqlalchemy.orm import Session
from app.models import Topic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status

class CreateTopic:
    @handle_errors
    def run(
        db: Session,
        topic_name: str,
        topicR: Repository[Topic]
    ):
        topic_name = topic_name.upper()

        topicR.create({'topic_name':topic_name})

        db.commit()

        return JSONResponse(status_code= status.HTTP_201_CREATED, content='Topic Created')

