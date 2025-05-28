from fastapi.testclient import TestClient
from uuid import uuid4 as uuid

from datetime import datetime, date, time
from app.main import app
from app.tests.utils import create_user, create_profesional, create_topic, create_student, del_topic, del_user, add_prof_topic
from unittest import TestCase


class TestReservation(TestCase):

    #Seteo que se hara antes de cualquier test
    def setUp(self):
        self.client = TestClient(app)
        
        # Se crea el usuario/profesional
        self.prof_id = 'professional' #str(uuid())
        # self.client.post('/users', json={'user_id': self.prof_id})
        # self.client.post('/professionals', json={'prof_id': self.prof_id})  
        create_user(self.prof_id)
        create_profesional(self.prof_id)

        #Se crea un topico 'griego'
        # self.client.post('/topics', json={'topic_name':'griego'})
        # self.client.post(f'/topics/professionals/{self.prof_id}', json={'prof_id':self.prof_id, 'topic_name':'griego', 'price_class': 20})
        
        create_topic('griego')
        add_prof_topic(self.prof_id, 'griego', 10)

        # Se crea un id para el student
        self.student_id = 'student' #str(uuid())

        #self.client.post('/users', json={'user_id':self.student_id})
        #S1 = self.client.post(f'/students/{self.student_id}')
        #self.assertEqual(S1.status_code, 200)

        create_user(self.student_id)
        create_student(self.student_id)

        # Como no hay EP, se debe agregar a Student a mano
        self.route = '/reservation'
        
    # Ejecucion luego de concluido el test
    # Elimina el usuario de profesionales, NO de Users
    def tearDown(self):
        #response = self.client.delete(f'/users/{self.prof_id}')
        #self.assertEqual(response.status_code, 200)
        #response = self.client.delete(f'/users/{self.student_id}')
        #elf.assertEqual(response.status_code, 200)
        del_user(self.prof_id)
        del_user(self.student_id)
        del_topic('griego')
        

    """def test_create_reservation_specific(self):
        #Creacion specific
        specific = {'prof_id': 'professional',
        'day': '2025-05-23',
        'start': '09:00',
        'end': '12:00',
        'topics': [
            'GRIEGO'
            ]
        }

        response = self.client.post(f'/specific',params= {'prof_id':self.prof_id}, json= specific)
        self.assertEqual(response.status_code, 201)

        #Creacion de reserva
        parametro = {'student_id': self.student_id}

        json_data = {
            'prof_id':self.prof_id,
            'topic': 'GRIEGO',
            'day_hour': '2025-05-23 10:00:00'
        }
        
        response = self.client.post(f'{self.route}/class', params= parametro, json= json_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),'Clase creada')

        response = self.client.delete(f'/topics/', params= {'topic_name':specific['topics'][0]})
        ic(response.json())
        self.assertEqual(response.status_code, 200)

    """
   
    def test_reservation_recurrent(self):
        print('Create class reservation, from recurrent')
        recurrent = {
        'week_day': 2,
        'start': '09:00',
        'end': '12:00',
        'topics': [
            'GRIEGO'
            ]
        }

        response = self.client.post(f'/recurrent',params= {'prof_id':self.prof_id}, json= recurrent)
        self.assertEqual(response.status_code, 201)

        #Creacion de reserva
        parametro = {'student_id': self.student_id}

        json_data = {
            'prof_id':self.prof_id,
            'topic': 'GRIEGO',
            'day_hour': '2025-05-13 10:00:00'
        }
        
        response = self.client.post(f'{self.route}/class', params= parametro, json= json_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),'Clase creada')


    def test_reservation_recurrent_not_topic(self):
        print('Create class reservation, from recurrent, with invalid topic')
        recurrent = {
        'week_day': 2,
        'start': '09:00',
        'end': '12:00',
        'topics': [
            'GRIEGO'
            ]
        }

        response = self.client.post(f'/recurrent',params= {'prof_id':self.prof_id}, json= recurrent)
        self.assertEqual(response.status_code, 201)

        #Creacion de reserva
        parametro = {'student_id': self.student_id}

        json_data = {
            'prof_id':self.prof_id,
            'topic': 'FRANCES',
            'day_hour': '2025-05-13 10:00:00'
        }
        
        response = self.client.post(f'{self.route}/class', params= parametro, json= json_data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error']['message'],'El profesional no tiene horario para esa clase')