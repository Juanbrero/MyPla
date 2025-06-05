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
            'price_class': float 
        }
    """
    @handle_errors
    def run(
        db: Session,
        topic_name:str,
        professional_topicR: Repository[ProfessionalTopic]
    ):
        
        professionals = professional_topicR.get_by({'topic_name':topic_name})

        data_professional = []
        for prof in professionals:
            data_professional.append(
                {'prof_id':prof.prof_id,
                 'price_class': prof.price_class
                 }
            )         
            
        

        return JSONResponse(status_code= status.HTTP_200_OK, content= data_professional)
        
