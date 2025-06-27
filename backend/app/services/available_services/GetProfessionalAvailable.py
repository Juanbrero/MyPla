from app.utils.errors import handle_errors
from app.models import SpecificSchedule, Class ,Reservation, RecurrentSchedule, Event,Invite
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import date, timedelta

class GetProfessionalAvailable():
    @handle_errors
    def run(
            db : Session,
            prof_id: str,
            recurrentR: Repository[RecurrentSchedule],
            exceptionR: Repository[SpecificSchedule],
            specificR: Repository[SpecificSchedule],
            classR: Repository[Class],
            reservationR: Repository[Reservation],
            eventR: Repository[Event],
            inviteR: Repository[Invite]
    ):
        reservationR.delPending()
        
        all_specifics = specificR.getAllWithTopics(prof_id, False)

        all_exceptions = exceptionR.getAllWithProfessional(prof_id)
        
        all_recurrents = recurrentR.getRecurrentsWithTopics(prof_id)

        all_class = classR.getTopicClass(prof_id)

       

        

        data_specific = []
        for schedule in all_specifics:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat(),
                "topics": [topic.topic_name for topic in schedule.topic_specifics]
            }
            data_specific.append(item)

        data_recurrent = []
        for schedule in all_recurrents:
            item = {
                "prof_id": schedule.prof_id,
                "week_day": schedule.week_day,
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat(),
                "topics": [topic.topic_name for topic in schedule.topic_recurrents]
            }
            data_recurrent.append(item)

        data_exception = []
        for schedule in all_exceptions:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat()
            }
            data_exception.append(item)
        
        data_class = []
        for schedule, student_id, topic_name, link in all_class:
            item ={
                "prof_id": schedule.prof_id,
                "student_id": student_id,
                "day_hour": schedule.day_hour.isoformat(),
                "topics": topic_name,
                "link_class": link
            }
            data_class.append(item) 

        all_events = eventR.getEventsHost(prof_id)

        data_events = []
        for event, topic in all_events:
            item ={
                "day_hour": event.day_hour.isoformat(),
                "end": (event.day_hour + timedelta(minutes= event.duration)).isoformat(),
                "topic": topic,
                "title": event.title
            }
            data_events.append(item)
        
        all_invites = inviteR.getProfInvitation(prof_id)

        data_invite = []
        for invite, title, username, topic in all_invites:
            item = {
                "host_username": username,
                "day_hour": invite.day_hour.isoformat(),
                "end": (invite.day_hour + timedelta(minutes=event.duration)).isoformat(),
                "topic": topic,
                "title": title
            }
            data_invite.append(item)

        response = {
            'specific': data_specific,
            'recurrent': data_recurrent,
            'exception': data_exception,
            'class_': data_class,
            'my_events': data_events,
            'guest': data_invite
        }
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
        
