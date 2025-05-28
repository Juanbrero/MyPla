from sqlalchemy.orm import Session
from app.models import ProfessionalTopic, Topic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic

class CreateProfTopic:
    @handle_errors
    def run(
        db: Session,
        prof_topicS: schema_prof_topic.ProfessionalTopic,
        professional_topicR: Repository[ProfessionalTopic],
        topicR: Repository[Topic]
    ):
        prof_topicS.topic_name = prof_topicS.topic_name.upper()

        topic = topicR.get_by({'topic_name':prof_topicS.topic_name})

        if len(topic) == 0:
            raise NotFound('Topic not exist')
        
        if prof_topicS.price_class <= 0:
            raise ValueError('Price value invalid')
        
        professional_topicR.create({
            'prof_id': prof_topicS.prof_id,
            'price_class': prof_topicS.price_class,
            'topic_name': prof_topicS.topic_name
        })

        db.commit()

        return JSONResponse(status_code= status.HTTP_201_CREATED, content='Professional topic add')


