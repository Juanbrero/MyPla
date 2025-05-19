from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4 

from fastapi import Depends
from app.bd.schemas import schema_topic_specific
from app.config.database import get_db
from app.repository.specific_repository import SpecificRepository
from app.models import SpecificSchedule

import requests

"""
Codigo que lee diferentes listas con diccionarios, y realiza las peticiones POST para cargar las tablas
"""

client = TestClient(app)

BASE_URL = "http://localhost:8002"

def test_root():
    print('Test root')
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "¡Hola, FastAPI está funcionando!"}




def charge_DB():

    def insert_user(usuarios):
    # Envío de usuarios
        for user in usuarios:
            response = requests.post(f"{BASE_URL}/users", json=user)
            print(f"Usuario {user}: {response.status_code} - {response.text}")

    def insert_profesional(profesionales):
        # Envío de profesionales
        for prof in profesionales:
            response = requests.post(f"{BASE_URL}/professionals", json=prof)
            print(f"Profesional {prof}: {response.status_code} - {response.text}")

    def insert_topics(topics):
        # Envío de topics
        for topic in topics:
            response = requests.post(f"{BASE_URL}/topics", json=topic)
            print(f"Tema {topic['topic_name']}: {response.status_code} - {response.text}")

    def insert_profesional_topic(profesionaltopico):
        # Envío de profesional-topico
        for entry in profesionaltopico:
            prof_id = entry['prof_id']
            body = {
                'topic_name': entry['topic_name'],
                'price_class': entry['price_class']
            }
            response = requests.post(f"{BASE_URL}/topics/professionals/{prof_id}", json=body)
            print(f"Prof-Topico {prof_id} - {entry['topic_name']}: {response.status_code} - {response.text}")

    def insert_recurrent(recurrentes):
        # Envío de horarios recurrentes
        for rec in recurrentes:
            prof_id = rec['prof_id']
            body = {
                'week_day': rec['week_day'],
                'start': rec['start'],
                'end': rec['end'],
                'topics': rec['topics']
            }
            response = requests.post(f"{BASE_URL}/professionals/{prof_id}/agenda/recurrent", json=body)
            print(f"Recurrente {prof_id} - {rec['week_day']}: {response.status_code} - {response.text}")

    def insert_specific(especificos):
        # Envío de horarios especificos
        for spec in especificos:
            prof_id = spec['prof_id']
            body = {
                'day': spec['day'],
                'start': spec['start'],
                'end': spec['end'],
                'topics': spec['topics']
            }
            response = requests.post(f"{BASE_URL}/professionals/{prof_id}/agenda/specific", json=body)
            print(f"Especifico {prof_id} - {spec['day']}: {response.status_code} - {response.text}")

    def insert_exception(excepcion):
        # Envío de horarios excepcionales
        for exc in excepcion:
            prof_id = exc['prof_id']
            body = {
                'day': exc['day'],
                'start': exc['start'],
                'end': exc['end'],
            }
            response = requests.post(f"{BASE_URL}/professionals/{prof_id}/agenda/exceptions", json=body)
            print(f"Excepción {prof_id} - {exc['day']}: {response.status_code} - {response.text}")

    def update_recurrent(update):
        for up in update:
            prof_id = up['prof_id']
            body = {
                'week_day': up['week_day'],
                'start': up['start'],
                'Nstart': up.get('Nstart',None),
                'Nend': up.get('Nend',None)
            }
            response = requests.put(f'{BASE_URL}/professionals/{prof_id}/agenda/recurrent', json=body)
            print(f'Recurrent Update {prof_id} - {up['week_day']}: {response.status_code} - {response.text}')

    usuarios = [{'user_id': 'a'},
                {'user_id': 'b'},
                {'user_id': 'z'}
    ]

    profesionales = [
        {'prof_id': 'a'},
        {'prof_id': 'z'},
        {'prof_id': 'b'}
    ]

    topics = [
        {'topic_name': 'ingles'},
        {'topic_name': 'frances'},
        {'topic_name': 'fisica'},
        {'topic_name': 'filosofia'}
    ]

    profesionaltopico = [
        {'prof_id': 'a',
      'topic_name': 'ingles', 
      'price_class': 1
      },
        {'prof_id': 'a',
      'topic_name': 'frances', 
      'price_class': 1
      },
        {'prof_id': 'z',
      'topic_name': 'filosofia', 
      'price_class': 1
      },
        {'prof_id': 'z',
      'topic_name': 'ingles', 
      'price_class': 2
      },
        {'prof_id': 'b',
      'topic_name': 'FIsica', 
      'price_class': 3
      }
    ]


    recurrentes = [
            {"prof_id": "a",
        "week_day": 2,
        "start": "00:30",
        "end": "02:30",
        "topics": [
            {
            "topic_name": "ingles"
            },
            {
            "topic_name": "frances"
            }
            ]
        },
            {"prof_id": "a",
        "week_day": 1,
        "start": "00:30",
        "end": "02:30",
        "topics": [
            {
            "topic_name": "ingles"
            },
            {
            "topic_name": "frances"
            }
            ]
        },
            {"prof_id": "z",
        "week_day": 1,
        "start": "17:30:20.443Z",
        "end": "18:30:20.443Z",
        "topics": [
            {
            "topic_name": "filosofia"
            }
            ]
        },
            {"prof_id": "z",
        "week_day": 2,
        "start": "15:30:20.443Z",
        "end": "23:30:20.443Z",
        "topics": [
            {
            "topic_name": "filosofia"
            },
            {
            "topic_name": "ingles"
            }
            ]

        }
    ]

    especificos = [
        {
            "prof_id": 'b',
            "day": "2025-04-30",
            "start": "20:30:25.443Z",
            "end": "22:30:25.443Z",
            "topics": [
                {
                "topic_name": "fisica"
                }
            ]
        }
    ]

    excepciones = [
        {
            'prof_id':'a',
            "start": "18:30:30.527Z",
            "end": "19:30:30.527Z",
            "day": "2025-05-02"
        }
    ]


    insert_user(usuarios)
    insert_profesional(profesionales)
    insert_topics(topics)
    insert_profesional_topic(profesionaltopico)
    insert_recurrent(recurrentes)
    insert_specific(especificos)
    insert_exception(excepciones)

    test = [{"prof_id": "a",
        "week_day": 5,
        "start": "00:00",
        "end": "00:00",
        "topics": [
            {
            "topic_name": "ingles"
            }
            ]
        }

    ]
    #insert_recurrent(test)

    update = [{
        'prof_id':'a',
        "week_day": 5,
        "start": '00:00',
        "Nstart": '17:00'
    }]
    
    #update_recurrent(update)


