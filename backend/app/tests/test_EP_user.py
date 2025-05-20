from app.main import app
from fastapi.testclient import TestClient
from uuid import uuid4  as uuid
from unittest import TestCase



class TestUserEP(TestCase):
    
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        dele = self.client.get('/users')
        for user in dele.json():
            self.client.delete(f'/users/{user['user_id']}')
        


    def test_insert_user(self):
        print('Test insert user "prueba" ')
        user = {'user_id': 'prueba'}
        response = self.client.post(url='/users', json=user)
        self.assertEqual( response.status_code, 200)
        self.assertEqual(response.json(), {'user_id': 'prueba', 'name': 'prueba'})



    def test_insert_user_error(self):
        print('Test re insertar "repito" Error')
        user = {'user_id': 'repito'}
        response = self.client.post(url='/users', json=user)
        
        user = {'user_id':'repito'}
        response = self.client.post(url='/users', json=user)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual( response.json(), {'detail': 'User already exist'})

    def test_get_one_user(self): 
        print('Test Get user "get"')
        user = {'user_id': 'get'}
        response = self.client.post(url='/users', json=user)

        user = 'get'
        response = self.client.get(f'/users/{user}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'user_id': 'get','name':'get'})

    def test_get_users(self):
        print('Test Get all Users')
        user = {'user_id': 'one'}
        response = self.client.post(url='/users', json=user)
        user = {'user_id': 'two'}
        response = self.client.post(url='/users', json=user)
        response = self.client.get(url='/users')
        assert response.status_code == 200
        assert response.json() == [{'user_id': 'one', 'name':'one'}, {'user_id': 'two', 'name':'two'}]

    def test_get_not_exist(self):
        user = uuid()
        print(f'Eliminacion usuario inexistente {user}')
        response = self.client.get(f'/users/{user}')
        assert response.status_code == 404
        assert response.json() == {'detail': 'User not found'}  


    def test_delete_not_user(self):
        print('Test eliminar usuario "no_existo"')
        user_id = 'no_existo'
        response = self.client.delete(url=f'/users/{user_id}')
        assert response.status_code == 404
        assert response.json() == {'detail': 'User not found'}

    def test_delete_exist_user(self):
        print('eliminar un usuario')
        user = {'user_id': 'delete'}
        response = self.client.post(url='/users', json=user)
        user_id = 'delete'
        
        response = self.client.delete(url=f'/users/{user_id}')
        assert response.status_code == 200
        assert response.json() == {'detail': 'User deleted sucessfully'}

