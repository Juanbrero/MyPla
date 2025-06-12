from app.utils.errors import handle_errors
from app.models import SpecificSchedule, Reservation , RecurrentSchedule
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_response
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import timedelta, date
from app.bd.bd_utils import week_convert
import calendar

class GetStudentAvailable():
    @handle_errors
    def run(
        db : Session,
        prof_id: str,
        day: date,
        student_id: str,
        recurrentR: Repository[RecurrentSchedule],
        exceptionR: Repository[SpecificSchedule],
        specificR: Repository[SpecificSchedule],
        reservationR: Repository[Reservation]
    ):
        if day is None:
            day = date.today()
        last_day = day + timedelta(days=7)

        all_recurrents = recurrentR.getRecurrentsWithTopics(prof_id)

        #RECURENT
        data_recurrent = []

        day_recurrent= date(year= day.year, month= day.month, day= day.day)

       

        """if day.month == 12:
            next_year = day.year + 1
            next_month= 1
        else:
            next_year = day.year
            next_month = day.month + 1

        last_day = date(
            next_year,
            next_month,
            calendar.monthrange(next_year, next_month)[1]
        )   """ 

        # Recorre desde el mes ingresado hasta el siguiente
        while day_recurrent <= last_day:
        
            # Recorre el recurrent y genera los horarios
            # 
            for schedule in all_recurrents:
                if week_convert(schedule.week_day) == day_recurrent.isoweekday():
                    item ={
                    "prof_id": schedule.prof_id,
                    "day": day_recurrent.isoformat(),
                    "start": schedule.start.isoformat(),
                    "end": schedule.end.isoformat(),
                    "topics": [topic.topic_name for topic in schedule.topic_recurrents]
                    }
                    data_recurrent.append(item)
                if week_convert(schedule.week_day) > day_recurrent.isoweekday():
                    break
            day_recurrent += timedelta( days= 1 )    


        

        # Hasta aca -> lista con los dias recurrentes ordenados
        # Specific -> Exception -> cancela recurrente y define horario especifo
        #          -> Amplia el horario de un profesional
        # R 12 - 18
        # S 12 - 15 E 15 - 18 <-
        # S 8 - 12
        # S 8 - 18
        data_available= []

        #SPECIFIC
        #day = day.replace(day=1)
        all_specifics = specificR.getHourDay(prof_id, day, last_day)

        data_specific = []
        index_r = 0
        for schedule in all_specifics:
            for dayr in range(index_r, len(data_recurrent)):
                
                if data_recurrent[dayr]["day"] < schedule.day.isoformat():
                    data_available.append(data_recurrent[dayr])
                elif data_recurrent[dayr]["day"] > schedule.day.isoformat():
                    
                    item = {
                        "prof_id": schedule.prof_id,
                        "day": schedule.day.isoformat(),
                        "start": schedule.start.isoformat(),
                        "end": schedule.end.isoformat(),
                        "topics": [topic.topic_name for topic in schedule.topic_specifics]
                    }
                    data_available.append(item)
                    index_r= dayr
                    break
                #mismo dia
                elif schedule.end.isoformat() <= data_recurrent[dayr]['start']:
                    item = {
                        "prof_id": schedule.prof_id,
                        "day": schedule.day.isoformat(),
                        "start": schedule.start.isoformat(),
                        "end": schedule.end.isoformat(),
                        "topics": [topic.topic_name for topic in schedule.topic_specifics]
                    }
                    data_available.append(item)
                    index_r= dayr
                    break
                elif schedule.start.isoformat() >= data_recurrent[dayr]['end']:
                    data_available.append(data_recurrent[dayr])
                    
            if index_r == len(data_recurrent) -1:
                item = {
                        "prof_id": schedule.prof_id,
                        "day": schedule.day.isoformat(),
                        "start": schedule.start.isoformat(),
                        "end": schedule.end.isoformat(),
                        "topics": [topic.topic_name for topic in schedule.topic_specifics]
                    }
                data_available.append(item)
        if index_r != len(data_recurrent) -1:
            data_available.extend(data_recurrent[index_r:])





        #EXCEPTION
        all_exceptions = exceptionR.getHourDay(prof_id, day, last_day)

        data_exception = []
        for schedule in all_exceptions:
            item = {
                "prof_id": schedule.prof_id,
                "day": schedule.day.isoformat(),
                "start": schedule.start.isoformat(),
                "end": schedule.end.isoformat()
            }
            data_exception.append(item)

       

        #RESERVATION
        all_reservation = reservationR.getReservationDayHour(prof_id, day, last_day)
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

        """
        Recorrer especificos y recurrentes
            -> exception.dia == especifico|recurrente
            => tomar info del dia, ver horas -> 
            R: 10 s:10 e: 15
            S: 10 s:8 e: 12
            E: 10 s:12 e: 15
            Res: 10 s: 8:30 e: 9:30
        """
        # IDEA DE exception
        for exception in data_exception:
            break
            for recurrent in data_recurrent:
                
                if exception['day'] == recurrent['day']:
                    # 10 == 10
                    if exception['start'] >= recurrent['start'] and exception['end'] <= recurrent['end']:
                        # 12 >= 10 and 15 <= 15
                        # 12 >= 8 and 15 <= 12
                        pass
                    
        #data_available = data_recurrent.copy()
        #data_available.extend(data_specific)


        response = {
            'available': data_available,
            'reserv': data_exception
        }

        
        """response = {
            'specific': data_specific,
            'recurrent': data_recurrent,
            'exception': data_exception
        }"""

        
        return JSONResponse(status_code= status.HTTP_200_OK, content= response)