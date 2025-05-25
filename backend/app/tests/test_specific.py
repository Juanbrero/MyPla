from fastapi.testclient import TestClient
from unittest import TestCase
from uuid import uuid4 as uuid
from datetime import date, time
from app.main import app
from fastapi.encoders import jsonable_encoder


class TestSpecificEP(TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.prof_id = str(uuid())
        U1 =self.client.post('/users', json={'user_id': self.prof_id})
        self.assertEqual(U1.status_code, 200)
        P1 = self.client.post('/professionals', json={'prof_id': self.prof_id})
        

    def tearDown(self):
        self.client.delete(f'/users/{self.prof_id}')
        

    def test_R_insert(self):
        print(f'Insert via /specific')

        R1 = self.client.post('/topics', json={'topic_name': 'GRIEGO'})
        self.assertEqual(R1.status_code, 200)
        
        R2 = self.client.post(f'/topics/professionals/{self.prof_id}', json={'topic_name':'GRIEGO', 'price_class': 20})
        self.assertEqual(R2.status_code, 200)
        data = {
            'start': '01:00',
            'end': '10:00',
            'day': '2025-03-03',
            'topics':[
                'GRIEGO'
            ]
        }

        response =  self.client.post(f'/specific/',params= {'prof_id':self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Specific created')
        
        response = self.client.delete(f'/topics/', params= {'topic_name':data["topics"][0]})
        self.assertEqual(response.status_code, 200)