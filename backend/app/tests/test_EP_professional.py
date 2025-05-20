from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4 as uuid
from unittest import TestCase


class TestProfessionalEP(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.user_id = str(uuid())
    
    def tearDown(self):
        dele = self.client.get('/users')
        for user in dele.json():
            self.client.delete(f'/users/{user['user_id']}')


    def test_create_professional(self):
        print(f'Crear un usuario y definirlo como professional {self.user_id}')
        user = {'user_id': self.user_id}
        response_user = self.client.post('/users', json= user)
        self.assertEqual(response_user.status_code, 200)

        professional = {'prof_id': user.get('user_id')}
        response_professional = self.client.post('/professionals', json= professional)
        self.assertEqual( response_professional.status_code, 200)
        self.assertEqual( response_professional.json(), {'info':f'Insert existos {professional.get('prof_id')}'})

    def test_delete_not_professional(self):
        print(f'Test delete profesional no existente')
        prof_id = self.user_id
        response_professional = self.client.delete(f'/professionals/{prof_id}')
        assert response_professional.status_code == 404
        assert response_professional.json() == {'detail': 'Professional not found'}


    def test_get_professional(self):
        print('Get all Professionals')
        self.client.post('/users', json={'user_id':self.user_id})
        self.client.post('professionals', json={'prof_id': self.user_id})
        response = self.client.get('/professionals')
        self.assertEqual( response.status_code, 200)
        self.assertEqual(response.json(),[{'prof_id':self.user_id, 'score':0}])
        
    
    def test_delete_professional(self):
        self.client.post('/users', json={'user_id':self.user_id})
        self.client.post('professionals', json={'prof_id': self.user_id})

        prof_id = self.user_id
        print(f'Test delete professional {prof_id}')
        response_professional = self.client.delete(f'/professionals/{prof_id}')
        self.assertEqual(response_professional.status_code, 200)
        self.assertEqual( response_professional.json(), {'detail': 'Professional deleted sucessfully'})

    



