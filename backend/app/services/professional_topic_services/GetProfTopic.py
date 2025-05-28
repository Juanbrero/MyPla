from sqlalchemy.orm import Session
from app.models import ProfessionalTopic, Topic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic


class GetProfTopic:
    @handle_errors
    def run(
        db: Session,
        prof_id: str,
        professional_topicR: Repository[ProfessionalTopic]
    ):
        
        all_topic = professional_topicR.get_by({'prof_id': prof_id})

        if len(all_topic)== 0:
            raise NotFound('Professional topics not found')
        
        result = [schema_prof_topic.ProfessionalTopic.from_orm(prof_topic).dict() for prof_topic in all_topic]


        return JSONResponse(status_code= status.HTTP_200_OK, content= result)