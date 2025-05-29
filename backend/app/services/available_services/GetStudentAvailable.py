from app.utils.errors import handle_errors
from app.models import SpecificSchedule, Reservation , RecurrentSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_response
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import timedelta, date

class GetStudentAvailable():
    @handle_errors
    def run(
        db = Session,
        prof_id= str,
        day= date,
        recurrentR= Repository[RecurrentSchedule],
        exceptionR= Repository[SpecificSchedule],
        specificR= Repository[SpecificSchedule],
        reservationR= Repository[Reservation]
    ):
        if day is None:
            day = date.today()

        all_specifics = specificR.getHourDay(prof_id, day)
    
        all_exceptions = exceptionR.getHourDay(prof_id, day)
        
        all_recurrents = recurrentR.getRecurrentsWithTopics(prof_id)
        
        all_reservation = reservationR.getReservationDayHour(prof_id, day)

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

        day_recurrent= date(year= day.year, month= day.month, day=1)
        month = day.month

        while day_recurrent.month == month:
            day_recurrent.isoweekday()
            day_recurrent.fr
            for schedule in all_recurrents:
                item = {
                    "prof_id": schedule.prof_id,
                    "week_day": schedule.week_day,
                    "start": schedule.start.isoformat(),
                    "end": schedule.end.isoformat(),
                    "topics": [topic.topic_name for topic in schedule.topic_recurrents]
                }
                data_recurrent.append(item)

            data_recurrent += timedelta(days=1)

        

        data_exception = []
        for schedule in all_exceptions:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat()
            }
            data_exception.append(item)

        for reservation in all_reservation:

            start = reservation.day_hour.time().strftime('%H:%M')
            end =   (reservation.day_hour + timedelta(hours=1)).time().strftime('%H:%M')
            day = reservation.day_hour.date()
          
            item = {
                "prof_id": reservation.prof_id,
                "day": day.isoformat(),
                "start": start,
                "end":end
            }
            data_exception.append(item)
        
        response = {
            'specific': data_specific,
            'recurrent': data_recurrent,
            'exception': data_exception
        }

        
        return JSONResponse(status_code= status.HTTP_200_OK, content= response)