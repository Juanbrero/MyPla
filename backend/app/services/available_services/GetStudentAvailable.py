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

        all_recurrents = recurrentR.getRecurrentsWithTopics(prof_id)

        #RECURENT
        data_recurrent = []

        day_recurrent= date(year= day.year, month= day.month, day= 1)
        month = day.month

        """days = {'1':[],
                '2':[],
                '3':[],
                '4':[],
                '5':[],
                '6':[],
                '7':[]}"""
        
        # Recorre desde el mes ingresado hasta el siguiente
        while day_recurrent.month <= (month + 1):
            # Agrega al diccionario los dias especificos en base al dia de la semana 

            """days[ str( day_recurrent.isoweekday() ) ].append( day_recurrent ) """
            
            # Recorre el recurrent y genera los horarios
            # 
            for schedule in all_recurrents:
                if schedule.week_day == day_recurrent.isoweekday():
                    item ={
                    "prof_id": schedule.prof_id,
                    "day": day_recurrent.isoformat(),
                    "start": schedule.start.isoformat(),
                    "end": schedule.end.isoformat(),
                    "topics": [topic.topic_name for topic in schedule.topic_recurrents]
                    }
                    data_recurrent.append(item)
                if schedule.week_day > day_recurrent.isoweekday():
                    break
            day_recurrent += timedelta( days= 1 )    

        """for schedule in all_recurrents:
            # Toma todos los dias de un dia de la semana
            # lunes[2025-..., 2025-..., ..]
            dias = days[str(schedule.week_day)]
            for dia in dias:
                item = {
                    "prof_id": schedule.prof_id,
                    "day": dia.isoformat(),
                    "start": schedule.start.isoformat(),
                    "end": schedule.end.isoformat(),
                    "topics": [topic.topic_name for topic in schedule.topic_recurrents]
                }
                data_recurrent.append(item)"""


        

        #SPECIFIC
        all_specifics = specificR.getHourDay(prof_id, day)

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


        #EXCEPTION
        all_exceptions = exceptionR.getHourDay(prof_id, day)

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
        all_reservation = reservationR.getReservationDayHour(prof_id, day)

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
        # IDEA DE excetion
        for exception in data_exception:
            break
            for recurrent in data_recurrent:
                
                if exception['day'] == recurrent['day']:
                    # 10 == 10
                    if exception['start'] >= recurrent['start'] and exception['end'] <= recurrent['end']:
                        # 12 >= 10 and 15 <= 15
                        # 12 >= 8 and 15 <= 12
                        pass



        
        response = {
            'specific': data_specific,
            'recurrent': data_recurrent,
            'exception': data_exception
        }

        
        return JSONResponse(status_code= status.HTTP_200_OK, content= response)