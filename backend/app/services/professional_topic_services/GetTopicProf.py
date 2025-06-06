from sqlalchemy.orm import Session
from app.models import ProfessionalTopic, Professional
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
        professional_topicR: Repository[ProfessionalTopic],
        professionalR: Repository[Professional]
    ):
        
        professionals = professional_topicR.get_by({'topic_name':topic_name})
        # Join con users para traer datos, salvo score

        data_professional = []
        for prof in professionals:
            user_data, score = professionalR.getInfo(prof.prof_id)
            data_professional.append(
                {'prof_id':prof.prof_id,
                 'price_class': prof.price_class,
                 'username': user_data.username,
                 'score': score
                 }
            )         
            
        

        return JSONResponse(status_code= status.HTTP_200_OK, content= data_professional)
        
