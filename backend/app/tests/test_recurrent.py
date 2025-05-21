from fastapi.testclient import TestClient
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from uuid import uuid4 as uuid

from datetime import date, time

from app.main import app
from app.bd.schemas import schema_topic_recurrent
from app.config.database import get_db
from app.repository.recurrent_repository import RecurrentRepository
from app.models import RecurrentSchedule
from unittest import TestCase
from random import randint


client = TestClient(app)

def get_db_repository():
    """
    Funcion que retorna la db
    """
    return next(get_db())


def create_professional(user_id: str):
    """
    Crea por endpoints un usuario professional
        Args:
            - user_id: str
        Return
            - user_id: str
    """
    user_id = str(user_id)
    #print(f'\n User Create')
    user = {'user_id':user_id}
    response_user = client.post('/users', json=user)
    response_user.status_code == 200
    response_user.json() == {'user_id': user_id, 'name': user_id}

    #print(f'Professional Create')
    professional = {'prof_id':user['user_id']}
    response_professional = client.post('/professionals', json= professional)
    response_professional.status_code == 200
    response_professional.json() == {'info':f'Insert existos {professional.get('prof_id')}'}
    print('------ >')
    return professional.get('prof_id')

def del_user (user_id:str):
    """
    Elimina un usuario
        Args:
            - user_id: str
        Returns:
            - 200
    """
    #print(f'< ----\nUser Delete')
    response_user = client.delete(f'/users/{user_id}')
    assert response_user.status_code == 200
    return 200


class TestRecurrentRepository(TestCase):

    def setUp(self):
        self.prof_id = create_professional(uuid())
        self.db = get_db_repository()
        self.recurrent_repository = RecurrentRepository(self.db)

    def tearDown(self):
        del_user(self.prof_id)

    def test_insert(self):
        """
        Se crea un dia recurrentet
        """
        print('Insertar un recurrente')
        
        recurrent = schema_topic_recurrent.RecurrentSchema( week_day= 1,
                                                            start=time(hour=10),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_recurrent_create = self.recurrent_repository.create(recurrent)
        self.assertEqual(obj_recurrent_create.prof_id, self.prof_id)

    def test_get_complete(self):
        """
        Recupera un dia Recurrent, pasando todos su PK
        """
        
        print('Get Recurrent Day (week_day, start)')
        
        recurrent = schema_topic_recurrent.RecurrentSchema( week_day=3,
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_recurrent_create = self.recurrent_repository.create(recurrent)

        obj_recurrent_get = self.recurrent_repository.get_recurrent_week_start(recurrent)
        dict_excep_test = schema_topic_recurrent.RecurrentCreate.from_orm(obj_recurrent_get)

        test_json = jsonable_encoder({
            'week_day': 3,
            'start':time(hour=9),
            'end': time(hour=12)
        })

        self.assertEqual( jsonable_encoder(dict_excep_test), test_json)
    
    def test_get_week(self):
        print('Get Recurrent Day (week_day)')
        recurrent = schema_topic_recurrent.RecurrentSchema( week_day=3,
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_recurrent_create = self.recurrent_repository.create(recurrent)

        obj_recurrent_get = self.recurrent_repository.get_recurrent_week(recurrent)
        dict_recurrent_test = [schema_topic_recurrent.RecurrentCreate.from_orm(obj) for obj in obj_recurrent_get]

        test_json = jsonable_encoder({
            'week_day': 3,
            'start':time(hour=9),
            'end': time(hour=12)
        })

        self.assertEqual( jsonable_encoder(dict_recurrent_test), [test_json])

    def test_get_prof(self):
        print('Get Recurrent Days (prof_id))')
        recurrent = schema_topic_recurrent.RecurrentSchema( week_day=5,
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_recurrent_create = self.recurrent_repository.create(recurrent)

        obj_get = schema_topic_recurrent.ProfessionalID(**recurrent.dict())
        obj_recurrent_get = self.recurrent_repository.get_recurrent(obj_get)

        dict_recurrent_test = [schema_topic_recurrent.RecurrentCreate.from_orm(obj) for obj in obj_recurrent_get]

        test_json = jsonable_encoder({
            'week_day': 5,
            'start':time(hour=9),
            'end': time(hour=12)
        })

        self.assertEqual( jsonable_encoder(dict_recurrent_test), [test_json])

    
      
    def test_update_start(self):
        """
        Actualizar hora de inicio
        """
        
        print('Update Recurrent start')
        
        
        recurrent_insert = schema_topic_recurrent.RecurrentSchema( week_day= 7,
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_recurrent_create = self.recurrent_repository.create(recurrent_insert)
       

        obj_recurrent_get = self.recurrent_repository.get_recurrent_week_start(recurrent_insert)
        
        recurrent_update = schema_topic_recurrent.RecurrentCreate(week_day= 7,
                                                            start=time(hour=7),
                                                            end= time(hour=12),
                                                            )
        

        obj_recu_update = self.recurrent_repository.update(obj_recurrent_get, recurrent_update)


        recu_test = schema_topic_recurrent.RecurrentCreate.from_orm(obj_recu_update)
        recurrent_test = jsonable_encoder(recu_test)
        dict_recurrent_update = jsonable_encoder(recurrent_update)

        self.assertEqual( recurrent_test, dict_recurrent_update)


    def test_update_end(self):
        """
        Actualizar hora de fin
        """
        
        print('Update Recurrent End')
        
        
        recurrent_insert = schema_topic_recurrent.RecurrentSchema( week_day= 3,
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        obj_recurrent_create = self.recurrent_repository.create(recurrent_insert)
       

        obj_recurrent_get = self.recurrent_repository.get_recurrent_week_start(recurrent_insert)
        
        recurrent_update = schema_topic_recurrent.RecurrentCreate(week_day= 3,
                                                            start=time(hour=9),
                                                            end= time(hour=23))
       

        recu_update = self.recurrent_repository.update(obj_recurrent_get, recurrent_update)


        recurrent_test = schema_topic_recurrent.RecurrentCreate.from_orm(recu_update)

        recurrent_test = jsonable_encoder(recurrent_test)
        dict_recurrent_update = jsonable_encoder(recurrent_update)

        self.assertEqual( recurrent_test, dict_recurrent_update)


    def test_update(self):
            """
            Actualizar hora de inicio y fin
            """
            db = get_db_repository()
            
            print('Update Recurrent Hour')
            
            
            recurrent_insert = schema_topic_recurrent.RecurrentSchema( week_day= 3,
                                                                start=time(hour=8),
                                                                end= time(hour=13),
                                                                prof_id= self.prof_id
                                                                )
            obj_recurrent_create = self.recurrent_repository.create(recurrent_insert)
        

            obj_recurrent_get = self.recurrent_repository.get_recurrent_week_start(recurrent_insert)
            
            recurrent_update = schema_topic_recurrent.RecurrentCreate(week_day= 3,
                                                                start=time(hour=6),
                                                                end= time(hour=22))
            

            recu_update = self.recurrent_repository.update(obj_recurrent_get, recurrent_update)


            recurrent_test = schema_topic_recurrent.RecurrentCreate.from_orm(recu_update)

            recu_test = jsonable_encoder(recurrent_test)
            dict_recurrent_update = jsonable_encoder(recurrent_update)

            self.assertEqual( recu_test, dict_recurrent_update)

    def test_delete(self):
        
        print('Delete Recurrent')
        
        recurrent_insert = schema_topic_recurrent.RecurrentSchema( week_day= 5,
                                                            start=time(hour=15),
                                                            end= time(hour=20),
                                                            prof_id= self.prof_id
                                                            )
        

        spec_create = self.recurrent_repository.create(recurrent_insert)
       

        obj_recu_get = self.recurrent_repository.get_recurrent_week_start(recurrent_insert)

        recu_delete = self.recurrent_repository.delete(obj_recu_get)
        recurrent_insert_dict = jsonable_encoder(recurrent_insert)
        
        self.assertTrue (recu_delete, recurrent_insert_dict)
    
    def test_isInclude(self):
        print('Is Include')
        recurrent = schema_topic_recurrent.RecurrentSchema( week_day= 2,
                                                            start=time(hour=10),
                                                            end= time(hour=18),
                                                            prof_id= self.prof_id
                                                            )
        
        self.recurrent_repository.create(recurrent)
        recurrent.start = time(hour=19)
        recurrent.end = time(hour=21)

        self.recurrent_repository.create(recurrent)

        times = [
                {'start': time(hour=8),
                'end': time(hour=12)},

                {'start': time(hour=7),
                'end': time(hour=9)},
                
                {'start': time(hour=7),
                'end': time(hour=10)},
                
                {'start': time(hour=10),
                'end': time(hour=17)},
                
                {'start': time(hour=11),
                'end': time(hour=13)},
                
                {'start': time(hour=18),
                'end': time(hour=20)},
                
                {'start': time(hour=11),
                'end': time(hour=19)},
                
                {'start': time(hour=11),
                'end': time(hour=17)},

                {'start': time(hour=10),
                'end': time(hour=18)}
                ]
        dict_recurrent = recurrent.dict()

        test = [True, False, False, True, True, True, True, True, True]

        for tim in range(len(times)):
            
            dict_recurrent.update(times[tim])
            include = schema_topic_recurrent.RecurrentSchema(**dict_recurrent)

            isInclude = self.recurrent_repository.isInclude(include)
            self.assertEqual(isInclude, test[tim], dict_recurrent)
            
    def test_isValid(self):
        print('Is Valid')
        test = [True, False, True]
        values = [{'start': time.fromisoformat('00:00'), 'end': time.fromisoformat('00:00')},
                  {'start': time.fromisoformat('10:00'), 'end': time.fromisoformat('09:00')},
                  {'start': time.fromisoformat('00:00'), 'end': time.fromisoformat('09:00')}]
        for v in range(len(values) - 1):
            response = self.recurrent_repository.isValidTime(values[v]['start'],values[v]['end'])
            self.assertEqual(response, test[v])
 
    def test_isCompleteHour(self):
        print('Is Complete Hour')
        print('10 Elements, first 5 Equal, last 5 random minutes + 1')
        tiempo = []
        for h in range(5):
            minuto = randint(0,59)
            tiempo.append(
            {'start':time(hour=10, minute=minuto), 'end':time(hour=10, minute=minuto)}
            )

        for h in range(5):
            minuto = randint(0, 58)
            tiempo.append(
            {'start':time(hour= 9, minute= minuto), 'end':time(hour= 9, minute= minuto + 1)}
            )

        for t in tiempo:
            print(t)
    
        for hora in range(5):
            response = self.recurrent_repository.isCompleteHour(tiempo[hora]['start'], tiempo[hora]['end'])
            self.assertTrue(response, tiempo[hora])
        for hora in range(5,10):
            response = self.recurrent_repository.isCompleteHour(tiempo[hora]['start'], tiempo[hora]['end'])
            self.assertFalse(response, tiempo[hora])

    def test_trunc_time(self):
        test = self.recurrent_repository.trunc_time(time.fromisoformat('20:01:23'))
        self.assertEqual(test, time.fromisoformat('20:01'))  



class TestRecurrentEP(TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        self.prof_id = create_professional(uuid())
    
    def tearDown(self):
        del_user(self.prof_id)


    def test_EP_insert_hour_incomplete(self):
        print(f' ERROR: Insert via /recurrents hora incompleta \n S:10:00 E:12:30')


        data = {
            'start': '10:00',
            'end': '12:30',
            'week_day': 3
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual( response.json(), {'detail': 'No es una hora completa'})

    def test_EP_insert_hour_invalid(self):
        print(f' ERROR: Insert via /recurrents hora incorrecta')
        print('End > Start')

        data = {
            'start': '13:00',
            'end': '10:00',
            'week_day': 4
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Start > End incorrect'})
    
    def test_EP_insert_week_invalid(self):
        print(f'Insert via /recurrents week_day invalid')
        print('week_day == 10')

        data = {
            'start': '1:00',
            'end': '00:00',
            'week_day': 10
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
               
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Week Day incorrect'})
    
    
    def test_EP_insert_E0_hour(self):
        print(f'Insert via /recurrents hora End: 0')
        print('End == 0')

        data = {
            'start': '1:00',
            'end': '00:00',
            'week_day': 4
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        test = jsonable_encoder({'start': time(hour=1),
            'end': time(hour=0),
            'week_day': 4,
            'prof_id': self.prof_id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_EP_insert_S0E0_hour(self):
        print(f'Insert via /recurrents hora start == end == 0')
        print('Start == End == 0')

        data = {
            'start': '0:00',
            'end': '00:00',
            'week_day': 4
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        test = jsonable_encoder(
            {'start': time(hour=0),
            'end': time(hour=0),
            'week_day': 4,
            'prof_id': self.prof_id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_EP_insert_two(self):
        print(f'Insert via /recurrents two idem recurrents')
        print('Two time idem recurrents')

        data = {
            'start': '0:00',
            'end': '00:00',
            'week_day': 6
        }
        self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        
        response = self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Day exist'}) 

    def test_EP_get_void(self):
        print('Get not day professional')

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/recurrents')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_EP_get_all(self):
        print('Get all days professional')

        data = {
            'start': '00:00',
            'end': '00:00',
            'week_day': 6
        }
        self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        
        response = self.client.get(f'/professionals/{self.prof_id}/agenda/recurrents')
        data.update({'prof_id':self.prof_id})
        test_value = {
            'week_day': data['week_day'],
            'start': time.fromisoformat(data['start']),
            'end': time.fromisoformat(data['end']),
            'prof_id': self.prof_id
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), jsonable_encoder([test_value]))

    def test_EP_get_week(self):
        print('Get all days week')

        data = {
            'start': '00:00',
            'end': '00:00',
            'week_day': 6
        }
        self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        
        response = self.client.get(f'/professionals/{self.prof_id}/agenda/recurrents/{data["week_day"]}')
        data.update({'prof_id':self.prof_id})
        test_value = {
            'week_day': data['week_day'],
            'start': time.fromisoformat(data['start']),
            'end': time.fromisoformat(data['end']),
            'prof_id': self.prof_id
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), jsonable_encoder([test_value]))

    
    def test_EP_update_None(self):
        print('ERROR: Update  None data')
        data = {
            'start': '10:00',
            'end': '13:00',
            'week_day': 5
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)
        update = {
            'start': '10:00',
            'week_day': 5
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Not update'})

    def test_EP_update_start(self):
        print('Update start')
        data = {
            'start': '10:00',
            'end': '13:00',
            'week_day': 5
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)   
        
        update = {
            'start': '10:00',
            'week_day': 5,
            'Nstart': '03:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('03:00'),
            'week_day': 5,
            'end': time.fromisoformat('13:00'),
            'prof_id': self.prof_id
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_update_end(self):
        print('Update end')
        data = {
            'start': '13:00',
            'end': '19:00',
            'week_day': 5
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)     
        update = {
            'start': '13:00',
            'week_day': 5,
            'Nend': '23:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('13:00'),
            'week_day': 5,
            'end': time.fromisoformat('23:00'),
            'prof_id': self.prof_id
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_update(self):
        print('Update Complete')
        data = {
            'start': '10:00',
            'end': '13:00',
            'week_day': 5
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)

        update = {
            'start': '10:00',
            'week_day': 5,
            'Nend': '19:00',
            'Nstart': '15:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)

        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('15:00'),
            'week_day': 5,
            'end': time.fromisoformat('19:00'),
            'prof_id': self.prof_id
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_update_not_complete(self):
        print('ERROR: Update Hour not complete')
        self.test_EP_insert_S0E0_hour()
        update = {
            'start': '00:00',
            'week_day': 4,
            'Nstart': '20:00',
            'Nend': '22:30'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'No es una hora completa'})
    
    def test_EP_update_not_valid(self):
        print('ERROR: Update start > end')
        self.test_EP_insert_S0E0_hour()
        update = {
            'start': '00:00',
            'week_day': 4,
            'Nstart': '22:00',
            'Nend': '20:00'
            
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Start > End incorrect'})

    def test_EP_update_include(self):
        print('ERROR: Update include')
        data = {
            'start': '00:00',
            'end': '10:00',
            'week_day': 5
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)

        data = {
            'start': '15:00',
            'end': '19:00',
            'week_day': 5
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)

        update = {
            'start': '00:00',
            'week_day': 5,
            'Nstart': '17:00',
            'Nend': '23:00'
        }

        response = self.client.put(f'/professionals/{self.prof_id}/agenda/recurrents', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Time incluide'})    


    def test_EP_not_delete(self):
        print('ERROR: Delete Recurrent not exist')
        data = {'start':'10:20', 'week_day': 5}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/recurrents', params=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail':'Day not found'})
    
    def test_EP_delete(self):
        print('Delete Recurrent')
        data = {
            'start': '15:00',
            'end': '19:00',
            'week_day': 3
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/recurrents', json= data)

        data = {'start':'15:00', 'week_day': 3}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/recurrents', params=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'detail':'Day deleted sucessfully'})

    def test_EP_delete_no_week(self):
        print('ERROR: Delete invalid week')
        data = {'start':'10:20', 'week_day': 10}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/recurrents', params=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Week value invalid'})