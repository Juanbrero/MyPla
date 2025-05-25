from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.models import RecurrentSchedule, Meeting
from app.bd.repositories.Repository import Repository
from sqlalchemy.orm import Session
from app.bd.schemas import schema_topic_recurrent
from datetime import timedelta
from app.bd.bd_utils import error_hand, Schedule, include_time, include_time1, valid_time, strip_time_hour_minute
from app.bd.schemas import schema_prof
from app.bd.cruds import crud_topic_recurrent
from fastapi.responses import JSONResponse
from fastapi import status


class UpRecurrent():
    @handle_errors
    def run(
        db:Session,
        recurrentS: schema_topic_recurrent.TopicRecurrentUpdate,
        recurrentR: Repository[RecurrentSchedule],
        meetingR: Repository[Meeting]
    ):
        
        if not recurrentS.week_day in range(1, 8):
            raise ValueError('Week is incorrect value')
        
        if recurrentS.Nstart is None and recurrentS.Nend is None:
            raise ValidationError('Not update information')
        
        recurrentS.start = strip_time_hour_minute(recurrentS.start)

        query = {
            'prof_id': recurrentS.prof_id,
            'week_day': recurrentS.week_day,
            'start': recurrentS.start
        }

        obj_to_update = recurrentR.get_by(
            query
        )

      
        if len(obj_to_update) == 0:
            raise NotFound('Recurrent not found')
        
        update = {
            'start': strip_time_hour_minute(nstart) if (nstart := recurrentS.Nstart) is not None else obj_to_update[0].start,
            'end': strip_time_hour_minute(nend) if (nend := recurrentS.Nend) is not None else obj_to_update[0].end
        }

        if not valid_time(Schedule(**update)):
            raise ValueError('Hour format is incorrect')
        
        meetings = meetingR.getMeetingRecurrent(recurrentS.prof_id, recurrentS.week_day, update['start'], update['end'])

        if len(meetings) > 0:
            raise ValidationError("In hour you have a meeting")
        
        list_week = recurrentR.getOmmit(
            query
        )

        for r in list_week:
            if not(update['end'] <= r.start or update['start'] >= r.end):
                raise ValidationError('Time is include in Recurrents')
        
        updated = recurrentR.update(update, query)

        db.commit()
        
        return JSONResponse(status_code=status.HTTP_200_OK, content='Recurrent updated')

        
