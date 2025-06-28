from app.utils.errors import handle_errors, ValidationError, NotFound
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.bd.schemas import schema_event
from app.bd.repositories.Repository import Repository
from datetime import datetime, timedelta
from app.models import Meeting, SpecificSchedule, RecurrentSchedule, Invite, Event, Professional, Topic
from fastapi import status

class CreateEvent:
    @handle_errors
    def run (
        db: Session,
        prof_id: str,
        meetingR: Repository[Meeting],
        professionalR: Repository[Professional],
        inviteR: Repository[Invite],
        eventR: Repository[Event],
        eventS: schema_event.EventBase,
        topicR: Repository[Topic]
    ):
        day = eventS.day_hour.date()
        start = eventS.day_hour.time()
        end = (eventS.day_hour + timedelta(minutes=eventS.duration)).time()
        
        m = meetingR.getMeetingToRange(
            prof_id=prof_id,
            day=day,
            start=start,
            end=end
        )
        
        if len(m) > 0:
            raise ValidationError("You have meeting in hour")
        
        t = topicR.get_by({"topic_name": eventS.topic})
        
        if len(t) <= 0:
            raise NotFound("Invalid Topic")
        
        meetingR.create({
            "day_hour": eventS.day_hour,
            "prof_id": prof_id,
            "topic_name": eventS.topic
        })
        
        db.flush()
        
        data_event = {
            "day_hour": eventS.day_hour,
            "prof_id": prof_id,
            "duration": eventS.duration,
            "price": eventS.price,
            "title": eventS.title
        }
        
        if len(eventS.invites) <= 0:
            data_event["confirm"] = True
        
        eventR.create(data_event)
        
        db.flush()
        
        for i in eventS.invites:
            if prof_id == i:
                ValidationError("You can't invite yourself")
                
            p = professionalR.get_by({
                "prof_id": i
            })

            if len(p) <= 0:
                NotFound("Invalid professionals")
        
        for i in eventS.invites:
            inviteR.create({
                "prof_id": prof_id,
                "day_hour": eventS.day_hour,
                "invite_id": i
            })
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Event created")