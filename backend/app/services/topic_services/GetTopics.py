from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from sqlalchemy.orm import Session
from app.models import Topic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status

class GetTopics:
    @handle_errors
    def run(
        db: Session,
        topicR: Repository[Topic]
    ):
        all_topics = topicR.get_all()

        response = [ topic.topic_name for topic in all_topics]

        return JSONResponse(status_code= status.HTTP_200_OK, content= response)