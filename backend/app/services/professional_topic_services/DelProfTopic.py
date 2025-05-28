from sqlalchemy.orm import Session
from app.models import ProfessionalTopic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic


class DelProfTopic:
    @handle_errors
    def run(
        db: Session,
        prof_topicS: schema_prof_topic.ProfessionalTopicDel,
        professional_topicR: Repository[ProfessionalTopic]
    ):
        prof_topicS.topic_name = prof_topicS.topic_name.upper()

        deleted= professional_topicR.delete({
            'prof_id': prof_topicS.prof_id,
            'topic_name': prof_topicS.topic_name
        })

        if deleted <= 0:
            raise NotFound('Professional topic not found')
        
        db.commit()

        return JSONResponse(status_code= status.HTTP_200_OK, content='Professional topic deleted')