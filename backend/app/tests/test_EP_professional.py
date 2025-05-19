from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4 

client = TestClient(app)


def test_create_professional():
    user_id_professional = str(uuid4())
    print(f'Crear un usuario y definirlo como professional {user_id_professional}')
    user = {'user_id': user_id_professional}
    response_user = client.post('/users', json= user)
    assert response_user.status_code == 200
    professional = {'prof_id': user.get('user_id')}
    response_professional = client.post('/professionals', json= professional)
    assert response_professional.status_code == 200
    assert response_professional.json() == {'info':f'Insert existos {professional.get('prof_id')}'}

def test_delete_not_professional():
    print(f'Test delete profesional no existente')
    prof_id = str(uuid4())
    response_professional = client.delete(f'/professionals/{prof_id}')
    assert response_professional.status_code == 200
    assert response_professional.json() == {'detail': 'Professional deleted sucessfully'}


def test_get_professional():
    print('Get all Professionals')
    response = client.get('/professionals')
    assert response.status_code == 200
    print(response.json())
    
 
def test_delete_professional():
    db_professional = client.get('/professionals')
    prof_id = db_professional.json()[0]['prof_id']
    print(f'Test delete professional {prof_id}')
    response_professional = client.delete(f'/professionals/{prof_id}')
    assert response_professional.status_code == 200
    assert response_professional.json() == {'detail': 'Professional deleted sucessfully'}

    response_delete = client.delete(f'/users/{prof_id}')
    assert response_delete.status_code == 200
    



