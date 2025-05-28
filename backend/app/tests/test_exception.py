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
        self.route = '/exception'
    
    def tearDown(self):
        del_user(self.prof_id)


    def test_valid_insertion(self):
        print(f'Insert via {self.route}')

        data = {
            'start': '01:00',
            'end': '10:00',
            'day': '2025-03-03'
        }

        response =  self.client.post(self.route,params= {'prof_id':self.prof_id}, json= data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 'Exception created')
        
    