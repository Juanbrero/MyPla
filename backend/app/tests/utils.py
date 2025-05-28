from app.config.database import get_db
from fastapi.testclient import TestClient
from app.main import app
from json import loads

def get_db_repository():
    """
    Funcion que retorna la db
    """
    return next(get_db())

client = TestClient(app)

def create_user(user_id: str):
    """
    Funcion que crea un usuario via /users
        Args:
            - user_id: str
        Return:
            - None
        JSON:
            - {'user_id': user_id}
    """
    user = {'user_id': user_id}
    response_user = client.post('/users', json= user)
    assert response_user.status_code == 200

def create_profesional(user_id: str) -> None:
    """
    Funcion que recibe un usuario y lo agrega a profesional via /professionals
        Args:
            - user_id: str
        Retun:
            None
        JSON:
            - {'prof_id': user_id}
    """
    professional = {'prof_id': user_id}
    response_professional = client.post('/professionals', json= professional)
    assert response_professional.status_code == 200

def create_student(user_id: str) -> None:
    """
    Funcion que recibe un usuario y lo agrega a student via /students
        Args:
            - user_id: str
        Retun:
            None
        /{user_id}
    """

    response_student = client.post(f'/students/{user_id}')
    assert response_student.status_code == 200

def del_user(user_id:str) -> None:
    """
    funcion que elimina un usuario via /users
        Args:
            - user_id:str
        Return:
            - None
    """
    response_user = client.delete(f'/users/{user_id}')
    assert response_user.status_code == 200

def create_topic(topic_name: str) -> str:
    topic = topic_name.upper()
    response_topic = client.post('/topics', json={'topic_name': topic})
    assert response_topic.status_code == 200
    return topic

def del_topic(topic_name: str) -> None:
    response_topic = client.delete('/topics/', params={'topic_name': topic_name})
    assert response_topic.status_code == 200

def add_prof_topic(prof_id: str, topic_name:str, price_class: float):
    response_prof_topic = client.post(f'/topics/professionals/{prof_id}', json={'topic_name': topic_name, 'price_class': price_class})
    assert response_prof_topic.status_code == 200

def error_message(response_body: bytes) -> str:
    """
    Fucion que decodifica el mensaje de error de un JSONResponse a str
        Args:
            - response.body: bytes
        Return:
            - message of error: str
    """
    return str(loads(response_body)['error']['message'])
