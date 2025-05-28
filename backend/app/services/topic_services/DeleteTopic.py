from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_topic
from sqlalchemy.orm import Session
from app.models import Topic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status


class DeleteTopic:
    @handle_errors
    def run(
        db: Session,
        topic_name: str,
        topicR: Repository[Topic]
    ):
        topic_name  = topic_name.upper()

        topic = topicR.delete({'topic_name':topic_name})

        if topic == 0:
            raise NotFound('Topic not found')
        
        db.commit()

        return JSONResponse(status_code= status.HTTP_200_OK, content='Topic deleted')