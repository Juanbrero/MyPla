from app.utils.errors import handle_errors, ValidationError, NotFound
from app.bd.schemas import schema_topic_specific
from sqlalchemy.orm import Session
from app.models import Meeting, SpecificSchedule, ProfessionalTopic, TopicSpecific, RecurrentSchedule
from app.bd.repositories.Repository import Repository
from app.bd.bd_utils import strip_time_hour_minute, week_convert
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import time

class UpdateSpecific:
    @handle_errors
    def run (
        db: Session, 
        specificS: schema_topic_specific.TopicSpecificUpdate, 
        specificR: Repository[SpecificSchedule],
        professional_topicR: Repository[ProfessionalTopic],
        topic_specificR: Repository[TopicSpecific],
        meetingR: Repository[Meeting],
        recurrentR: Repository[RecurrentSchedule]
    ):
        specificS.start = strip_time_hour_minute(specificS.start)
        
        old_specific = specificR.get_by({
            "day": specificS.day,
            "start": specificS.start
        })
        
        if (len(old_specific) <= 0):
            raise NotFound("Specific disponibility not exist")
        
        
        if specificS.Nday or specificS.Nend or specificS.Nstart:
            
            start = specificS.Nstart if specificS.Nstart else specificS.start
            start = strip_time_hour_minute(start)
            
            if specificS.Nend:

                specificS.Nend = strip_time_hour_minute(specificS.Nend)
                
                """if specificS.Nend.hour == 0:
                    specificS.Nend = time(hour=23, minute=59)"""
               
                if start >= specificS.Nend:
                    raise ValidationError("The range hour is invalid")
            
           
            
            day = specificS.Nday if specificS.Nday else specificS.day
            end = specificS.Nend if specificS.Nend else old_specific[0].end


            if start.minute != end.minute:
                raise ValidationError('Hour incomplete')
            
            specifics = specificR.getSpecificsToRange(specificS.prof_id, day, start, end)
            # Valido si existe otro specific en el rango, en caso de que haya uno deberia chequear si no es el mismo que envio el usuario 
            if len(specifics) > 1 or (len(specifics) == 1 and (specificS.day != specifics[0].day or specificS.start != specifics[0].start)):
                raise ValidationError("In hour you have hour specific to disponibility or exception")
            
            meetings = meetingR.getMeetingToRange(specificS.prof_id, day, start, end)
            if len(meetings) > 0:
                raise ValidationError("In hour you have a meeting")
            
            recurrent = recurrentR.getSpecific(
            {
                'prof_id': specificS.prof_id,
                'week': week_convert(day.isoweekday()),
                'start': start,
                'end': end
            }
            )
            if len(recurrent) != 0:
                raise ValidationError('Recurrent day found')
            
            specificR.update({
                "day": day,
                "start": start,
                "end": end
            }, {
                "day": specificS.day,
                "start": specificS.start,
                "prof_id": specificS.prof_id,
            })
        
        if specificS.topics:    
            if not professional_topicR.checkTopicProf(specificS.prof_id, specificS.topics):
                raise ValidationError("You don't have a topic")
            
            topics = topic_specificR.get_by({
                "day": day,
                "start": start,
                "prof_id": specificS.prof_id
            })
            
            topic_names = {top.topic_name for top in topics}
            
            topic_add = [s for s in specificS.topics if s not in topic_names]
            
            topic_set = set(specificS.topics)
            
            topic_remove = [top.topic_name for top in topics if top.topic_name not in topic_set]
            
            for t in topic_remove:
                topic_specificR.delete({
                    "prof_id": specificS.prof_id,
                    "start": start,
                    "day": day,
                    "topic_name": t
                })
            
            for t in topic_add:
                topic_specificR.create({
                    "prof_id": specificS.prof_id,
                    "start": start,
                    "day": day,
                    "topic_name": t
                })
        
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content="Specific modified")
        
        
        