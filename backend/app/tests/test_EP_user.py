from app.main import app
from fastapi.testclient import TestClient
from uuid import uuid4 


client = TestClient(app)


def test_insert_user():
    print('Test insert user "prueba" ')
    user = {'user_id': 'prueba'}
    response = client.post(url='/users', json=user)
    assert response.status_code == 200
    assert response.json() == {'user_id': 'prueba', 'name': 'prueba'}


def test_insert_user_error():
    print('Test re insertar "prueba" Error')
    user = {'user_id':'prueba'}
    response = client.post(url='/users', json=user)
    assert response.status_code == 400
    assert response.json() == {'detail': 'User already exist'}

def test_get_one_user(): 
    print('Test Get user "prueba"')
    user = 'prueba'
    response = client.get(f'/users/{user}')
    assert response.status_code == 200
    assert response.json() == {'user_id': 'prueba','name':'prueba'}

def test_get_users():
    print('Test Get all Users')
    response = client.get(url='/users')
    assert response.status_code == 200
    assert response.json() == [{'user_id': 'prueba', 'name':'prueba'}]

def test_get_not_exist():
    user = uuid4()
    print(f'Eliminacion usuario inexistente {user}')
    response = client.get(f'/users/{user}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}  


def test_delete_not_user():
    print('Test eliminar usuario "no_existo"')
    user_id = 'no_existo'
    response = client.delete(url=f'/users/{user_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_delete_exist_user():
    print('eliminar un usuario')
    user_id = 'prueba'
    response = client.delete(url=f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted sucessfully'}

