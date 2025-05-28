from fastapi.testclient import TestClient
from uuid import uuid4 as uuid

from datetime import datetime, date, time
from app.main import app
from app.tests.utils import create_user, create_profesional, create_topic, create_student, del_topic, del_user, add_prof_topic
from unittest import TestCase

class TestEndpointGET(TestCase):

    def setUp(self):
        self.prof_id = str(uuid())
        self.client = TestClient(app)
        create_user(self.prof_id)
        create_profesional(self.prof_id)
        self.route_available = '/available/professionals'
        self.route_specifics = '/specific'
        self.route_exceptions = '/exception'
        self.route_recurrents = '/recurrent'
    
    def tearDown(self):
        del_user(self.prof_id)


    def test_get_all(self):
        topic = create_topic('Judo')
        add_prof_topic(self.prof_id, topic, 20)

        json_specific = {'start': '01:00',
            'end': '10:00',
            'day': '2025-03-03',
            'topics':[
                topic
            ]

        }

        json_exception ={
            'start': '01:00',
            'end': '10:00',
            'day': '2025-03-05'
        }

        json_recurrent = {
            'start': '01:00',
            'end': '10:00',
            'week_day': 2,
            'topics':[
                topic
            ]

        }   
        parametro = {
            'prof_id': self.prof_id
        }

        response_specific = self.client.post(self.route_specifics, params= parametro, json= json_specific)
        self.assertEqual(response_specific.status_code, 201)

        response_exception = self.client.post(self.route_exceptions, params= parametro, json= json_exception)
        self.assertEqual(response_exception.status_code, 201)

        response_recurrent = self.client.post(self.route_recurrents, params= parametro, json= json_recurrent)
        self.assertEqual(response_recurrent.status_code, 201)
        
        response_available = self.client.get(self.route_available, params= parametro)
        
       
        self.assertEqual(response_available.status_code, 200)

        
        self.assertDictEqual(response_available.json(),{
            'recurrent':[{'prof_id': self.prof_id,
                          'start': '01:00:00',
            'end': '10:00:00',
            'week_day': 2,
            'topics':[
                topic
            ]}],
            'specific':[{'prof_id': self.prof_id,
                         'start': '01:00:00',
            'end': '10:00:00',
            'day': '2025-03-03',
            'topics':[
                topic
            ]}],
            'exception': [{'prof_id': self.prof_id,
            'start': '01:00:00',
            'end': '10:00:00',
            'day': '2025-03-05'}],
            'class': [],
            'event': []
        })
        
        del_topic(topic)
