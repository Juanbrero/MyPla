from fastapi.testclient import TestClient
from uuid import uuid4 as uuid

from datetime import time
from app.main import app

from unittest import TestCase
from app.controllers.RecurrentController import RecurrentController
from app.controllers.TopicRecurrentController import TopicRecurrentController
from app.tests.utils import get_db_repository, create_user, create_profesional, del_user, create_topic, del_topic, add_prof_topic, error_message
from random import random, randint
from app.bd.schemas import schema_topic_recurrent
from fastapi.encoders import jsonable_encoder
import json

class TestRepository(TestCase):
    def setUp(self):
        self.recurrentC = RecurrentController(get_db_repository())
        self.prof_id = str(uuid())
        create_user(self.prof_id)
        create_profesional(self.prof_id)
        self.topic = create_topic(str(uuid()))
        add_prof_topic(prof_id= self.prof_id, topic_name= self.topic, price_class= (randint( 1, 50) + random()))
        self.topic_recurrentC = TopicRecurrentController(get_db_repository())
        print()

    def tearDown(self):
        del_user(self.prof_id)
        del_topic(self.topic)
        
    #INSERT
    def test_create(self):
        print('Valid insertion')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '9:00',
            end= '10:00',
            week_day= 2,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

    def test_create_week_error(self):
        print('Inserción de semana invalida')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '9:00',
            end= '10:00',
            week_day= 0,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
        
    
        
        response_error = error_message(response.body)
        self.assertEqual(response.status_code, 400)
        
        # Para obtener el mensaje de error, se debe convertir el valor del body, por medio de json a un diccionario
        # Luego se accede al diccionario error -> message
        
        #json_response = jsonable_encoder(response)
        #value = json.loads(response['body'])['error']['message']
        
        self.assertEqual(response_error, 'Week value is incorrect')
    
    def test_create_minute_start_error(self):
        print('Insert invalid minute start 03:15')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '03:15',
            end= '10:00',
            week_day= 1,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
        
        
        self.assertEqual(response.status_code, 406)
       
        
        message = error_message(response.body)
        
        self.assertEqual(message, 'Not accept value minute, minute valid 00 or 30')

    def test_create_minute_end_error(self):
        print('Invalid minute end 10:23')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '03:00',
            end= '10:23',
            week_day= 1,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
        
        self.assertEqual(response.status_code, 406)
        
        message = error_message(response.body)
        
        self.assertEqual(message, 'Not accept value minute, minute valid 00 or 30')

    def test_create_schedule_incomplete_start_error(self):
        print('Insert incomplete schedule 9:30-12:00')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '9:30',
            end= '12:00',
            week_day= 1,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
        
        self.assertEqual(response.status_code, 400)
        
        response_error = error_message(response.body)
        
        self.assertEqual(response_error, 'The schedule must be full hours')
    
    def test_create_schedule_incomplete__end_error(self):
        print('Insert invalid schedule 10:00-15:30')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '10:00',
            end= '15:30',
            week_day= 1,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
        
              
        self.assertEqual(response.status_code, 400)
        
        response_error = error_message(response.body)
        
        self.assertEqual(response_error, 'The schedule must be full hours')
   
    def test_create_week_minute_error(self):
        print('Insert with week (0) and invalid hour 10:23 ')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '03:00',
            end= '10:23',
            week_day= 0,
            topics= [self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
    
       
        self.assertEqual(response.status_code, 400)
        
        message = error_message(response.body)
        self.assertEqual(message, 'Week value is incorrect')

    def test_create_invalid_schedule(self):
        print('Invalid schedule S= 11:00 E= 09:00')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00',
            end= '09:00',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
    
       
        self.assertEqual(response.status_code, 400)
        
        message = error_message(response.body)
        self.assertEqual(message, 'Hour format is incorrect')

    def test_create_end_0(self):
        print('Insert complete day S= 00:00 E= 00:00')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '00:00',
            end= '00:00',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

    def test_create_include(self):
        print('Insert complete day and insert S= 10:00 E= 15:00')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '00:00:15',
            end= '00:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        recurrentS1 = schema_topic_recurrent.TopicRecurrentIn(
            start= '10:00',
            end= '15:00',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )
        response = self.recurrentC.createRecurrent(recurrentS1)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body), 'Time is include in Recurrent') 
        
    def test_create_with_topics(self):
        print('Insert many topics')

        create_topic('Frances')
        add_prof_topic(self.prof_id, 'FRANCES', 15)
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '09:00:15',
            week_day= 6,
            prof_id= self.prof_id,
            topics=[self.topic, 'FRANCES']
        )
        response = self.recurrentC.createRecurrent(recurrentS)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        del_topic('France')
    
    def test_create_not_topic(self):
        print('Insert with not topic from professional')
        
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '09:00:15',
            week_day= 6,
            prof_id= self.prof_id,
            topics=['GRIEGO']
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 404)
        self.assertEqual(error_message(response.body), 'GRIEGO not is from Professional')

    
    def test_create_with_invalid_topics(self):
        print('Insert one topic valid, one invalid')

        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '09:00:15',
            week_day= 6,
            prof_id= self.prof_id,
            topics=[self.topic, 'FRANCES']
        )
        response = self.recurrentC.createRecurrent(recurrentS)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(error_message(response.body), 'FRANCES not is from Professional')
        del_topic('FRANCES')

    def test_create_not_professional_topic(self):
        print('Insert one topic valid, one exist but not from professional')
        create_topic('FRANCES')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '09:00:15',
            week_day= 6,
            prof_id= self.prof_id,
            topics=[self.topic, 'FRANCES']
        )
        response = self.recurrentC.createRecurrent(recurrentS)
    
        self.assertEqual(response.status_code, 404)
        self.assertEqual(error_message(response.body), 'FRANCES not is from Professional')
        del_topic('FRANCES')


    def test_create_not_topic(self):
        print('Insert void topics')

        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '09:00:15',
            week_day= 6,
            prof_id= self.prof_id,
            topics=[]
        )
        response = self.recurrentC.createRecurrent(recurrentS)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body), 'Recurrent day need topics')


    #GET         
    def test_get(self):
        print('Get week schedule')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')
        
        get = schema_topic_recurrent.TopicRecurrentWeekGet(prof_id= recurrentS.prof_id, week_day= recurrentS.week_day)
        response = self.recurrentC.getRecurrentWeek(get)
        
        self.assertListEqual(response,[{
            'week_day':6,
            'start': time(hour=11),
            'end':time(hour=12),
            'topics':[self.topic]
        }])

    def test_get_void_week(self):
        print('Get week without schedule')

        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        get = schema_topic_recurrent.TopicRecurrentWeekGet(prof_id= recurrentS.prof_id, week_day= 5)
        response = self.recurrentC.getRecurrentWeek(get)
        
        self.assertListEqual(response, [])


    def test_get_not_week(self):
        print('Get not week schedule')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')
        
        get = schema_topic_recurrent.TopicRecurrentWeekGet(prof_id= recurrentS.prof_id, week_day= 10)
        response = self.recurrentC.getRecurrentWeek(get)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body),'Week value is incorrect')

    # Update
    def test_update_not_data(self):
        print('Update hour, not information')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = {}
        
        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 500)


    def test_update_not(self):
        print('Update hour, not information')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body),'Not update information')

    def test_update_invalid_start(self):
        print('Update hour, invalid star hour')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nstart= '7:15:20'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(error_message(response.body),'Not accept value minute, minute valid 00 or 30')

    def test_update_invalid_end(self):
        print('Update hour, invalid end hour')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nend= '13:15:20'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(error_message(response.body),'Not accept value minute, minute valid 00 or 30')

    def test_update_invalid_schedule(self):
        print('Update hour, invalid hour')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nstart= '17:00:20',
            Nend= '10:00:50'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body),'Hour format is incorrect')

    def test_update_start(self):
        print('Update hour, start')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nstart= '10:00:20'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body),'Recurrent updated')


    def test_update_end(self):
        print('Update hour, end')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nend= '10:00:20'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body),'Recurrent updated')


    def test_update_include(self):
        print('Update hour, end')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        recurrentS1 = schema_topic_recurrent.TopicRecurrentIn(
            start= '18:00:15',
            end= '21:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS1)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nstart= '19:00:20',
            Nend= '20:00:00'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body),'Time is include in Recurrents')


    def test_update_week_not_exist(self):
        print('Update hour, week informtaion not exist')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= 3,
            Nstart= '12:00:20',
            Nend= '13:00:50'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(error_message(response.body),'Recurrent not found')

    def test_update_invalid_week(self):
        print('Update hour, week informtaion not exist')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')

        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= 12,
            Nstart= '13:00:20',
            Nend= '17:00:50'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body),'Week value is incorrect')

    def test_update_complete(self):
        print('Update hour, start and end')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '05:00:15',
            end= '15:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')


        update = schema_topic_recurrent.TopicRecurrentUpdate(
            prof_id= self.prof_id,
            start= recurrentS.start,
            week_day= recurrentS.week_day,
            Nstart= '19:00:20',
            Nend= '20:00:00'
        )

        response = self.recurrentC.updateRecurrent(update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body),'Recurrent updated')

    def test_add_topic(self):
        print('Add topic to recurrent day')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')
        
        create_topic('JAPONES')
        add_prof_topic(self.prof_id, 'JAPONES', 3)
        
        topic_recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= recurrentS.start,
            end= recurrentS.end,
            week_day= recurrentS.week_day,
            prof_id= recurrentS.prof_id,
            topics=['JAPONES']
        )
        
        response = self.topic_recurrentC.addTopic(topic_recurrentS)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), 'Recurrent topics updated')
        
        del_topic('JAPONES')

    def test_add_topic_invalid(self):
        print('Try add topic not from professional')
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')
        
        create_topic('JAPONES')
        add_prof_topic(self.prof_id, 'JAPONES', 3)
        
        topic_recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= recurrentS.start,
            end= recurrentS.end,
            week_day= recurrentS.week_day,
            prof_id= recurrentS.prof_id,
            topics=['JAPONES','SUECO']
        )
        
        response = self.topic_recurrentC.addTopic(topic_recurrentS)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(error_message(response.body), 'SUECO not is from Professional')
        
        del_topic('JAPONES')

    def test_del_topic(self):
        print('Del topic of recurrent day')
        create_topic('JAPONES')
        add_prof_topic(self.prof_id, 'JAPONES', 3)

        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic,'JAPONES'],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')
        
        
        topic_recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= recurrentS.start,
            end= recurrentS.end,
            week_day= recurrentS.week_day,
            prof_id= recurrentS.prof_id,
            topics=['JAPONES']
        )
        
        response = self.topic_recurrentC.delTopic(topic_recurrentS)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), 'Recurrent topics deleted')
        del_topic('JAPONES')

    def test_last_topic(self):
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '11:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')      
        

        response = self.topic_recurrentC.delTopic(recurrentS)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body),'Delete all topics not possible')  
        

    #DELETE

    def test_delete_valid(self):
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '01:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')  

        delete = schema_topic_recurrent.TopicRecurrentSchema(prof_id= self.prof_id,
                                                             start= recurrentS.start,
                                                             week_day= recurrentS.week_day)

        response = self.recurrentC.delRecurrent(delete)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), 'Recurrent deleted')

    def test_delete_invalid(self):
        recurrentS = schema_topic_recurrent.TopicRecurrentIn(
            start= '01:00:15',
            end= '12:00:15',
            week_day= 6,
            topics=[self.topic],
            prof_id= self.prof_id
        )

        response = self.recurrentC.createRecurrent(recurrentS)
       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), 'Recurrent created')  

        delete = schema_topic_recurrent.TopicRecurrentSchema(prof_id= self.prof_id,
                                                             start= recurrentS.start,
                                                             week_day= 10)

        response = self.recurrentC.delRecurrent(delete)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message(response.body), 'Week value is incorrect')

class TestEndpoint(TestCase):
     
    def setUp(self):
        self.client = TestClient(app)
        self.prof_id = str(uuid())
        create_user(self.prof_id)
        create_profesional(self.prof_id)

        #U1 = self.client.post('/users', json={'user_id': self.prof_id})
        #self.assertEqual(U1.status_code, 200)
        #P1 = self.client.post('/professionals', json={'prof_id': self.prof_id})
        

    def tearDown(self):
        del_user(self.prof_id)
        #self.client.delete(f'/users/{self.prof_id}')


    def test_insert(self):
        topic = create_topic('griego') 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '01:00',
            'end': '10:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        del_topic(topic)


    def test_get(self):
        topic = create_topic(str(uuid())) 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '01:00',
            'end': '10:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        

        response = self.client.get('/recurrent/', params={'prof_id':self.prof_id, 'week_day': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'end':'10:00:00',
                                             'start':'01:00:00',
                                               'week_day':2, 
                                               'topics':[topic]}])
        del_topic(topic)

    
    def test_update_not(self):
        topic = create_topic(str(uuid())) 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '01:00',
            'end': '10:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        json_data = {
            'week_day': 2,
            'start': '1:00'
        }
       
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error')['message'], 'Not update information')
        del_topic(topic)

    def test_update_start(self):
        topic = create_topic(str(uuid())) 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '01:00',
            'end': '10:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')

        json_data = {
            'week_day': 2,
            'start': '1:00',
            'Nstart': '5:00'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent updated')
        del_topic(topic)

    def test_del(self):
        topic = create_topic(str(uuid())) 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '01:00',
            'end': '10:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        response = self.client.delete('/recurrent/', params={'prof_id':self.prof_id, 'week_day': 2, 'start':'1:00'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent deleted')
        del_topic(topic)
