from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_topic_specific
from sqlalchemy.orm import Session
from app.models import Meeting, SpecificSchedule, ProfessionalTopic, TopicSpecific
from app.bd.repositories.Repository import Repository
from app.bd.bd_utils import strip_time_hour_minute
from fastapi.responses import JSONResponse
from fastapi import status

class CreateSpecific:
    @handle_errors
    def run (
        db: Session, 
        specificS: schema_topic_specific.TopicSpecificIn, 
        specificR: Repository[SpecificSchedule],
        professional_topicR: Repository[ProfessionalTopic],
        topic_specificR: Repository[TopicSpecific],
        meetingR: Repository[Meeting]
    ):
        specificS.start = strip_time_hour_minute(specificS.start)
        specificS.end = strip_time_hour_minute(specificS.end)
        
        if specificS.start >= specificS.end:
            raise ValidationError("The range hour is invalid")

        specifics = specificR.getSpecificsToRange(specificS.prof_id, specificS.day, specificS.start, specificS.end)
        if len(specifics) > 0:
            raise ValidationError("In hour you have hour specific to disponibility or exception")
        
        meetings = meetingR.getMeetingToRange(specificS.prof_id, specificS.day, specificS.start, specificS.end)
        if len(meetings) > 0:
            raise ValidationError("In hour you have a meeting")
        
        if not professional_topicR.checkTopicProf(specificS.prof_id, specificS.topics):
            raise ValidationError("You don't have a topic")
        
        specificR.create({
            "day": specificS.day,
            "start": specificS.start,
            "end": specificS.end,
            "prof_id": specificS.prof_id,
            "isCanceling": False
        })
        
        for topic in specificS.topics:
            topic_specificR.create({
                "day": specificS.day,
                "start": specificS.start,
                "topic_name": topic,
                "prof_id": specificS.prof_id
            })
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Specific created")
        
        
        