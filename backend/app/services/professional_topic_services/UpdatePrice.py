from sqlalchemy.orm import Session
from app.models import ProfessionalTopic, Topic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic

class UpdatePrice:
    @handle_errors
    def run(
        db: Session,
        prof_topicS: schema_prof_topic.ProfessionalTopic,
        professional_topicR: Repository[ProfessionalTopic]
    ):
        prof_topicS.topic_name = prof_topicS.topic_name.upper()

        prof_topic = professional_topicR.get_by({
            'prof_id': prof_topicS.prof_id,
            'topic_name': prof_topicS.topic_name
        })

        if len(prof_topic) == 0:
            raise NotFound('Professional topic not found')
        
        if prof_topicS.price_class <= 0:
            raise ValueError('Price value is invalid')
        
        updated= professional_topicR.update(values={'price_class':prof_topicS.price_class}, 
                                   filters={'prof_id': prof_topicS.prof_id,
            'topic_name': prof_topicS.topic_name})
        
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content='Price of topic updated')