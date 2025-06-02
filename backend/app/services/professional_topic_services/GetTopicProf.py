from sqlalchemy.orm import Session
from app.models import ProfessionalTopic
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_prof_topic


class GetTopicProf:
    """
    Return
       - { 'prof_id': str,
            'topics': list[str] 
        }
    """
    @handle_errors
    def run(
        db: Session,
        professional_topicR: Repository[ProfessionalTopic]
    ):
        
        professionals = professional_topicR.get_all()

        data_professional = []
        
        prof = 0
        while prof <= len(professionals) - 1:
            topics = []
            prof_id= professionals[prof].prof_id
            while prof <= len(professionals) - 1 and prof_id == professionals[prof].prof_id:
                topics.append(professionals[prof].topic_name)
                prof += 1
            data_professional.append({
                'pro_id': prof_id,
                'topics': topics})             
            
        

        return JSONResponse(status_code= status.HTTP_200_OK, content= data_professional)
        
