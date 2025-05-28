from app.utils.errors import handle_errors, NotFound
from app.bd.schemas import schema_topic_specific
from sqlalchemy.orm import Session
from app.models import SpecificSchedule, TopicSpecific
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status


class DeleteSpecific:
    @handle_errors
    def run (
        db: Session, 
        specificS: schema_topic_specific.TopicSpecificDeleteIn, 
        specificR: Repository[SpecificSchedule],
        topic_specificR: Repository[TopicSpecific],
    ):
        specific = specificR.get_by({
            "day": specificS.day,
            "prof_id": specificS.prof_id,
            "start": specificS.start
        })
        
        if (len(specific) <= 0):
            raise NotFound("Specific day hour not exist")
        
        topic_specificR.delete({
            "day": specificS.day,
            "prof_id": specificS.prof_id,
            "start": specificS.start
        })
        
        specificR.delete({
            "day": specificS.day,
            "prof_id": specificS.prof_id,
            "start": specificS.start
        })
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content="Specific deleted")
        