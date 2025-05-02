"""
crea un codigo que lea una lista llamada usuarios con diccionarios {'user_id':USER_ID}, y el contenido del mismo lo envie por un POST enpoint /create/{user_id}, donde el USER_ID ira en el path de la url en lugar de {user_id}
crea un codigo que lea una lista llamada profesionales con diccionarios {'id_prof':PROF_ID}, y los envia a por un POST endpoint /profesional/{id_prof}/create, donde el PROF_ID ira en el path
crea un codigo que lea una lista llamada topics con diccionarios {'topic_name':TOPIC_NAME}, y lo envia por un POST dentro del body  al enpoint /topics/create
crea un codigo que lea una lista llamada profesionaltopico con un diccionario {'prof_id':PROF_ID, 'topic_name':TOPIC_NAME, 'price_class': PRICE}, con un POST /topics/add/prof/{PROF_ID}, colocando el PROF_ID en el path, y crando un diccionario con el demas contenido del diccionario original
Crea un codigo que lea una lista llamada recurrentes con un diccionario {    'id_prof': PROF_ID,  "week_day": WEEK,  "start": START,  "end": END,  "topics": [    {      "topic_name": TOPIC    }  ]}, con un POST a prof/{PROF_ID}/agenda/test, colocando el PROF_ID del diccionario en el path, y creando el body con el resto del diccionario
"""

import requests

BASE_URL = "http://localhost:8002"

def test_user(usuarios):
    # Envío de usuarios
    for user in usuarios:
        user_id = user['user_id']
        response = requests.post(f"{BASE_URL}/create/{user_id}")
        print(f"Usuario {user_id}: {response.status_code} - {response.text}")

def test_profesional(profesionales):
    # Envío de profesionales
    for prof in profesionales:
        prof_id = prof['id_prof']
        response = requests.post(f"{BASE_URL}/professional/{prof_id}/create")
        print(f"Profesional {prof_id}: {response.status_code} - {response.text}")

def test_topics(topics):
    # Envío de topics
    for topic in topics:
        response = requests.post(f"{BASE_URL}/topics/create", json=topic)
        print(f"Tema {topic['topic_name']}: {response.status_code} - {response.text}")

def test_profesional_topic(profesionaltopico):
    # Envío de profesional-topico
    for entry in profesionaltopico:
        prof_id = entry['prof_id']
        body = {
            'topic_name': entry['topic_name'],
            'price_class': entry['price_class']
        }
        response = requests.post(f"{BASE_URL}/topics/prof/{prof_id}/add", json=body)
        print(f"Prof-Topico {prof_id} - {entry['topic_name']}: {response.status_code} - {response.text}")

def test_recurrent(recurrentes):
    # Envío de horarios recurrentes
    for rec in recurrentes:
        prof_id = rec['id_prof']
        body = {
            'week_day': rec['week_day'],
            'start': rec['start'],
            'end': rec['end'],
            'topics': rec['topics']
        }
        response = requests.post(f"{BASE_URL}/prof/{prof_id}/agenda/create/recurrent", json=body)
        print(f"Recurrente {prof_id} - {rec['week_day']}: {response.status_code} - {response.text}")

def test_specific(especificos):
    # Envío de horarios especificos
    for spec in especificos:
        prof_id = spec['id_prof']
        body = {
            'day': spec['day'],
            'start': spec['start'],
            'end': spec['end'],
            'topics': spec['topics']
        }
        response = requests.post(f"{BASE_URL}/prof/{prof_id}/agenda/create/spec", json=body)
        print(f"Especifico {prof_id} - {spec['day']}: {response.status_code} - {response.text}")

def test_exception(excepcion):
    # Envío de horarios excepcionales
    for exc in excepcion:
        prof_id = exc['prof_id']
        body = {
            'day': exc['day'],
            'start': exc['start'],
            'end': exc['end'],
        }
        response = requests.post(f"{BASE_URL}/prof/{prof_id}/agenda/create/exception", json=body)
        print(f"Excepción {prof_id} - {exc['day']}: {response.status_code} - {response.text}")

if __name__=='__main__':
    usuarios = [{'user_id': 'a'},
                {'user_id': 'b'},
                {'user_id': 'z'}
    ]

    profesionales = [
        {'id_prof': 'a'},
        {'id_prof': 'z'},
        {'id_prof': 'b'}
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
            {"id_prof": "a",
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
            {"id_prof": "a",
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
            {"id_prof": "z",
        "week_day": 1,
        "start": "17:30:20.443Z",
        "end": "18:30:20.443Z",
        "topics": [
            {
            "topic_name": "filosofia"
            }
            ]
        },
            {"id_prof": "z",
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
            "id_prof": 'b',
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


    test_user(usuarios)
    test_profesional(profesionales)
    test_topics(topics)
    test_profesional_topic(profesionaltopico)
    test_recurrent(recurrentes)
    test_specific(especificos)
    test_exception(excepciones)