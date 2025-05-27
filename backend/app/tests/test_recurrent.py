from fastapi.testclient import TestClient
from uuid import uuid4 as uuid

from datetime import time
from app.main import app

from unittest import TestCase
from app.controllers.RecurrentController import RecurrentController
from app.tests.utils import get_db_repository, create_user, create_profesional, del_user, create_topic, del_topic, add_prof_topic, error_message
from random import random, randint
from app.bd.schemas import schema_topic_recurrent
from fastapi.encoders import jsonable_encoder
import json


class TestEndpointPOST(TestCase):
     
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

    # POST
    def test_insert_valid(self):
        print('Insert via /recurrent/, correct')
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

    def test_insert_invalid_week(self):
        print('Insert via /recurrent/, with invalid week value')
        topic = create_topic('ALPHA')
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)

        data = {
            'start': '13:00',
            'end': '15:00',
            'week_day': 30,
            'topics': [
                topic
            ]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Week value is incorrect')
        del_topic(topic)

    def test_insert_invalid_start(self):
        print('Insert via /recurrent/, with invalid hour start')
        topic = create_topic('BETA')
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        data = {
            'start': '13:20',
            'end': '15:00',
            'week_day': 3,
            'topics': [
                topic
            ]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json()['error']['message'], 'Not accept value minute, minute valid 00 or 30')
        del_topic(topic)

    def test_insert_invalid_end(self):
        print('Insert via /recurrent/, with invalid hour end')
        topic = create_topic('BETA')
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        data = {
            'start': '10:00',
            'end': '16:33',
            'week_day': 3,
            'topics': [
                topic
            ]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json()['error']['message'], 'Not accept value minute, minute valid 00 or 30')
        del_topic(topic)

    def test_insert_week_hour(self):
        print('Insert via /recurrent/, with invalid week and hour')
        topic = create_topic('BETA')
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        data = {
            'start': '10:00',
            'end': '16:22',
            'week_day': -5,
            'topics': [
                topic
            ]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Week value is incorrect')
        del_topic(topic)

    def test_insert_invalid_schedule(self):
        print('Insert via /recurrent/, with invalid schedule')
        topic = create_topic('BETA')
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        data = {
            'start': '16:00',
            'end': '01:00',
            'week_day': 6,
            'topics': [
                topic
            ]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Hour format is incorrect')
        del_topic(topic)

    def test_insert_E_0(self):
        print('Insert via /recurrent/, with End= 0')
        topic = create_topic('BETA')
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        data = {
            'start': '12:00',
            'end': '00:00',
            'week_day': 7,
            'topics': [
                topic
            ]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        del_topic(topic)

    def test_insert_topics(self):
        print('Insert via /recurrent/, with 5 topics')
        topics = []
        for i in range(5):
            topic = create_topic(str(uuid()))
            topics.append(topic)
            add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 5)
        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': topics
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        for topic in topics:
            del_topic(topic)

    def test_insert_topic_not_exist(self):
        print('Insert via /recurrent/, with unknown')
    
        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': ['topic']
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error']['message'], 'topic is not of the Professional')

    def test_insert_topic_not_professional(self):
        print('Insert via /recurrent/, with unknown')
        topic = create_topic(str(uuid()))
        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': [topic]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error']['message'], f'{topic} is not of the Professional')
        del_topic(topic)



class TestEndpointGET(TestCase):
     
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

    # GET
    def test_get_valid(self):
        print('Get /recurrent/ week hours')
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

    def test_get_valid_not_schedule(self):
        print('Get /recurrent/ week, with not schedule')
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
        

        response = self.client.get('/recurrent/', params={'prof_id':self.prof_id, 'week_day': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        del_topic(topic)

    def test_get_invalid_week(self):
        print('Get /recurrent/ week')
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
        

        response = self.client.get('/recurrent/', params={'prof_id':self.prof_id, 'week_day': -10})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Week value is incorrect')
        del_topic(topic)

    def test_get_valid_many_schedule(self):
        print('Get /recurrent/ week, with two schedules')
        topic = create_topic(str(uuid())) 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '00:00',
            'end': '05:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')

        data1 = {
            'start': '10:30',
            'end': '15:30',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data1)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        

        response = self.client.get('/recurrent/', params={'prof_id':self.prof_id, 'week_day': 2})
        
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(),[{'start':'00:00:00',
                                             'end':'05:00:00',
                                               'week_day':2, 
                                               'topics':[topic]},
                                               {'end':'15:30:00',
                                             'start':'10:30:00',
                                               'week_day':2, 
                                               'topics':[topic]}] )
        del_topic(topic)


class TestEndpointPUT(TestCase):
     
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

    #PUT
    def test_update_void(self):
        print('Update /recurrent/, without data to update')
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

    def test_update_invalid_time_start(self):
        print('Update via /recurrent/, with invalid time start')
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
            'Nstart': '5:20'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json()['error']['message'], 'Not accept value minute, minute valid 00 or 30')
        del_topic(topic)

    def test_update_invalid_time_end(self):
        print('Update via /recurrent/, with invalid time end')
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
            'Nend': '10:45'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json()['error']['message'], 'Not accept value minute, minute valid 00 or 30')
        del_topic(topic)


    def test_update_invalid_schedule(self):
        print('Update via /recurrent/, with invalid schedule')
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
            'Nstart': '22:00',
            'Nend': '12:00'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Hour format is incorrect')
        del_topic(topic)


    def test_update_start(self):
        print('Update start via /recurrent/')
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

    def test_update_end(self):
        print('Update end via /recurrent/')
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
            'Nend': '5:00'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent updated')
        del_topic(topic)

    def test_update_not_time(self):
        print('Update via /recurrent/, not exist recurrent')
        json_data = {
            'week_day': 2,
            'start': '1:00',
            'Nstart': '5:00'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error']['message'], 'Recurrent not found')

    def test_update_with_include(self):

        topic = create_topic(str(uuid())) 
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 20)
        
        data = {
            'start': '00:00',
            'end': '05:00',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')

        data1 = {
            'start': '10:30',
            'end': '15:30',
            'week_day': 2,
            'topics':[
                topic
            ]
        }
        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data1)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')

        update = {
            'week_day': 2,
            'start': '00:00',
            'Nstart': '11:00',
            'Nend': '22:00'
        }

        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= update)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Time is include in Recurrents')


        del_topic(topic)

        



    def test_update_equal_time(self):
        print('Update via /recurrent/, with equal time')
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
            'Nstart': '1:00',
            'Nend':'10:00'
        }
        
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent updated')
        del_topic(topic)

    def test_update_invalid_week(self):
        print('Update /recurrent/, without week invalid')
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
            'week_day': 100,
            'start': '1:00'
        }
       
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= json_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error')['message'], 'Week value is incorrect')
        del_topic(topic)

    def test_update_topic_add(self):
        print('Update add topic /recurrent/')
        topic = create_topic(str(uuid()))
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 22)

        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': [topic]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        create_topic('API')
        add_prof_topic(prof_id= self.prof_id, topic_name= 'API', price_class= 5)
        topic_add ={
            'start': '10:00',
            'week_day': 2, 
            'topics': [topic, 'API']
        } 

        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json=topic_add)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent updated')

        del_topic('API')
        del_topic(topic)

    def test_update_topic_add_invalid(self):
        topic = create_topic(str(uuid()))
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 22)

        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': [topic]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        create_topic('API')
        topic_add ={
            'start': '10:00',
            'week_day': 2,
            'topics': ['API']
        } 
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json=topic_add)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], "You don't have a topic")

        del_topic('API')
        del_topic(topic)

    def test_update_topic_del(self):
        topics = []
        for i in range(5):
            topic = create_topic(str(uuid()))
            topics.append(topic)
            add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 5)
        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': topics
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        value = topics.pop(randint(0, 4))
        
        
        topic_del ={
            'start': '10:00',
            'week_day': 2,
            'topics': topics
        } 
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json=topic_del)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent updated')

        
        for topic in topics:
            del_topic(topic)


    def test_update_topic_add_del(self):
        topics = []
        for i in range(5):
            topic = create_topic(str(uuid()))
            topics.append(topic)
            add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 5)
        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': topics
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        value = topics.pop(randint(0, 4))
        topics.pop(randint(0, 3))
       
        create_topic('API')
        add_prof_topic(self.prof_id, 'API', 52)

        
        topics.append('API')
        
        topic_del ={
            'start': '10:00',
            'week_day': 2,
            'topics': topics
        } 
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json=topic_del)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Recurrent updated')


        for topic in topics:
            del_topic(topic)

    def test_update_topic_empty(self):

        topic = create_topic(str(uuid()))
        add_prof_topic(prof_id= self.prof_id, topic_name= topic, price_class= 22)

        data = {
            'start': '10:00',
            'end': '22:00',
            'week_day': 2,
            'topics': [topic]
        }

        response = self.client.post('/recurrent/', params={'prof_id': self.prof_id}, json= data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Recurrent created')
        
        
        topic_add ={
            'start': '10:00',
            'week_day': 2,
            'topics': []
        } 
        response = self.client.put('/recurrent/', params={'prof_id': self.prof_id}, json= topic_add)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Not update information')

        del_topic('API')
        del_topic(topic)


class TestEndpointDELETE(TestCase):
     
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

    # DELETE
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

    def test_del_not_exist(self):
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
        
        response = self.client.delete('/recurrent/', params={'prof_id':self.prof_id, 'week_day': 6, 'start':'1:00'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error']['message'], 'Recurrent day not exist')
        del_topic(topic)


    def test_del_invalid(self):
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
        
        response = self.client.delete('/recurrent/', params={'prof_id':self.prof_id, 'week_day': 200, 'start':'1:00'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['message'], 'Week value is incorrect')
        del_topic(topic)