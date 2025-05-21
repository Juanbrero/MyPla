from fastapi.testclient import TestClient
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from uuid import uuid4 as uuid

from datetime import date, time

from app.main import app
from app.bd.schemas import schema_topic_specific
from app.config.database import get_db
from app.repository.specific_repository import SpecificRepository
from app.models import SpecificSchedule
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

class TestSpecificRepository(TestCase):

    
    def setUp(self):
        self.prof_id = create_professional(uuid())
        self.db = get_db_repository()
        self.specific_repository = SpecificRepository(self.db)

    def tearDown(self):
        del_user(self.prof_id)
        
    def test_specific_insert(self):
        """
        Se crea un dia especifico
        """
        print('Insertar un Specific')
        
        specific = schema_topic_specific.SpecificSchema( day=date(year=2025, month=1, day=23),
                                                            start=time(hour=10),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )

        obj_spec_create = self.specific_repository.create(specific)
        self.assertEqual(obj_spec_create.prof_id, self.prof_id)
        self.assertEqual( obj_spec_create.isCanceling, False) 
        

    def test_specific_get_complete(self):
        """
        Recupera un dia Specific, pasando todos su PK
        """
        
        print('Get Specific Day')
        
        specific = schema_topic_specific.SpecificSchema( day=date(year=2025,month=1,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_specific_create = self.specific_repository.create(specific)

        obj_spec_get = self.specific_repository.get_day(specific)
        dict_spec_test = schema_topic_specific.SpecificGet.from_orm(obj_spec_get)

        test_json = jsonable_encoder({
            'day': date(year=2025,month=1,day=23),
            'start':time(hour=9),
            'end': time(hour=12),
            'prof_id': self.prof_id,
            'isCanceling': False
        })

        self.assertEqual( jsonable_encoder(dict_spec_test), test_json)

    def test_specific_get_day(self):
        """
        Recupera todos los horarios de un dia Specific
        """
        
        print('Get Specific Day')
        
        specific = schema_topic_specific.SpecificSchema( day=date(year=2025,month=1,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_specific_create = self.specific_repository.create(specific)
        obj_spec_get = self.specific_repository.get_day(specific)
        dict_spec_test = schema_topic_specific.SpecificGet.from_orm(obj_spec_get)

        test_json = jsonable_encoder({
            'day': date(year=2025,month=1,day=23),
            'start':time(hour=9),
            'end': time(hour=12),
            'prof_id': self.prof_id,
            'isCanceling': False
        })

        self.assertEqual( jsonable_encoder(dict_spec_test), test_json)

    def test_specific_get_month(self):
        """
        Recupera todos los dias especifico de un mes particular
            - prof_id
            - month
        Anio, se considera como actual
        """
        

        print('Get Specific Day from Month')
        

        specific = schema_topic_specific.SpecificSchema( day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        obj_spec_create = self.specific_repository.create(specific)
       
        specific_MY = schema_topic_specific.TopicSpecificMonthYear(prof_id= self.prof_id,
                                                                month= 6)

        list_obj_spec_get = self.specific_repository.get_month_year(specific_MY)
        test = [{
            'day': date(year=2025,month=1,day=23),
            'start':time(hour=9),
            'end': time(hour=12),
            'prof_id': self.prof_id,
            'isCanceling': False
        }]
        self.assertGreater(len(list_obj_spec_get), 0)

        for spec in range(len(list_obj_spec_get) - 1):
            spec_test = schema_topic_specific.SpecificGet.from_orm(spec_test[spec])
            test_value = test[spec]
            self.assertEqual( jsonable_encoder(spec_test), jsonable_encoder(test_value))

    def test_specific_get_hours(self):
        print('Get hours from one day')
        specific = schema_topic_specific.SpecificSchema( day=date(year=2025,month=9,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        obj_spec_create = self.specific_repository.create(specific)

        spec_get = schema_topic_specific.SpecificDayID(day=specific.day, prof_id= specific.prof_id)
        list_hours = self.specific_repository.get_day_hours(spec_get)
        dict_test = specific.dict()
        dict_test.update({'isCanceling':False})
        list(dict_test)
        for spec in range(len(list_hours) -1):
            spec_dict = schema_topic_specific.SpecificGet.from_orm(list_hours[spec])
            test_value = dict_test[spec]
            self.assertAlmostEqual(spec_dict, test_value)



    def test_specific_get_not_year(self):
        """
        Error de buscar dias especificos con un año inexistente
        """
        
        print('Get Specific Day from Not exist Year')
               
        
        specific_MY = schema_topic_specific.TopicSpecificMonthYear(prof_id= self.prof_id,
                                                                month= 6,
                                                                year= 2024)
        
        list_spec_get = self.specific_repository.get_month_year(specific_MY)

        self.assertEqual(len(list_spec_get), 0)
       

    def test_specific_update_start(self):
        """
        Actualizar hora de inicio
        """
        
        print('Update Specific start')
        
        
        specific_insert = schema_topic_specific.SpecificSchema( day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_spec_create = self.specific_repository.create(specific_insert)
       

        obj_spec_get = self.specific_repository.get_day(specific_insert)
        # Se utiliza el esquema SpecificGet, pero se ignora el isCanceling
        spec_update = schema_topic_specific.SpecificGet(day=date(year=2025,month=6,day=23),
                                                            start=time(hour=7),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id,
                                                            isCanceling=False)
        

        specific_update = self.specific_repository.update(obj_spec_get, spec_update)


        spec_test = schema_topic_specific.SpecificGet.from_orm(specific_update)
        spec_test = jsonable_encoder(spec_test)
        dict_spec_update = jsonable_encoder(spec_update)

        self.assertEqual( spec_test, dict_spec_update)


    def test_specific_update_end(self):
        """
        Actualizar hora de fin
        """
        
        print('Update Specific End')
        
        
        specific_insert = schema_topic_specific.SpecificSchema( day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        obj_spec_create = self.specific_repository.create(specific_insert)
       

        obj_spec_get = self.specific_repository.get_day(specific_insert)
        # Se utiliza el esquema SpecificGet, pero se ignora el isCanceling
        spec_update = schema_topic_specific.SpecificGet(day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=23),
                                                            prof_id= self.prof_id,
                                                            isCanceling=False)
       

        specific_update = self.specific_repository.update(obj_spec_get, spec_update)


        spec_test = schema_topic_specific.SpecificGet.from_orm(specific_update)

        spec_test = jsonable_encoder(spec_test)
        dict_spec_update = jsonable_encoder(spec_update)

        self.assertEqual( spec_test, dict_spec_update)


    def test_specific_update(self):
            """
            Actualizar hora de inicio y fin
            """
            db = get_db_repository()
            
            print('Update Specific Hour')
            
            
            specific_insert = schema_topic_specific.SpecificSchema( day=date(year=2025,month=6,day=23),
                                                                start=time(hour=8),
                                                                end= time(hour=13),
                                                                prof_id= self.prof_id
                                                                )
            obj_spec_create = self.specific_repository.create(specific_insert)
        

            obj_spec_get = self.specific_repository.get_day(specific_insert)
            # Se utiliza el esquema SpecificGet, pero se ignora el isCanceling
            spec_update = schema_topic_specific.SpecificGet(day=date(year=2025,month=6,day=23),
                                                                start=time(hour=6),
                                                                end= time(hour=22),
                                                                prof_id= self.prof_id,
                                                                isCanceling=False)
            

            specific_update = self.specific_repository.update(obj_spec_get, spec_update)


            spec_test = schema_topic_specific.SpecificGet.from_orm(specific_update)
            spec_test = jsonable_encoder(spec_test)
            dict_spec_update = jsonable_encoder(spec_update)

            self.assertEqual( spec_test, dict_spec_update)


    def test_specific_delete(self):
        
        print('Delete Specific')
        
        specific_insert = schema_topic_specific.SpecificSchema( day=date(year=2024,month=7,day=8),
                                                            start=time(hour=15),
                                                            end= time(hour=20),
                                                            prof_id= self.prof_id
                                                            )
        

        spec_create = self.specific_repository.create(specific_insert)
       

        obj_spec_get = self.specific_repository.get_day(specific_insert)

        spec_delete = self.specific_repository.delete(obj_spec_get)
        specific_insert_dict = jsonable_encoder(specific_insert)
        
        self.assertTrue (spec_delete, specific_insert_dict)
    
    def test_isInclude(self):
        print('Is Include')
        specific = schema_topic_specific.SpecificSchema( day=date(year=2025,month=1,day=1),
                                                            start=time(hour=10),
                                                            end= time(hour=18),
                                                            prof_id= self.prof_id
                                                            )
        
        self.specific_repository.create(specific)
        specific.start = time(hour=19)
        specific.end = time(hour=21)

        self.specific_repository.create(specific)

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
        dict_specific = specific.dict()

        test = [True, False, False, True, True, True, True, True, True]

        for tim in range(len(times)):
            
            dict_specific.update(times[tim])
            include = schema_topic_specific.SpecificSchema(**dict_specific)

            isInclude = self.specific_repository.isInclude(include)
            self.assertEqual(isInclude, test[tim], dict_specific)
            
    def test_isValid(self):
        print('Is Valid')
        test = [True, False, True]
        values = [{'start': time.fromisoformat('00:00'), 'end': time.fromisoformat('00:00')},
                  {'start': time.fromisoformat('10:00'), 'end': time.fromisoformat('09:00')},
                  {'start': time.fromisoformat('00:00'), 'end': time.fromisoformat('09:00')}]
        for v in range(len(values) - 1):
            response = self.specific_repository.isValidTime(values[v]['start'],values[v]['end'])
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
            response = self.specific_repository.isCompleteHour(tiempo[hora]['start'], tiempo[hora]['end'])
            self.assertTrue(response, tiempo[hora])
        for hora in range(5,10):
            response = self.specific_repository.isCompleteHour(tiempo[hora]['start'], tiempo[hora]['end'])
            self.assertFalse(response, tiempo[hora])

    def test_trunc_time(self):
        test = self.specific_repository.trunc_time(time.fromisoformat('20:01:23'))
        self.assertEqual(test, time.fromisoformat('20:01'))  

class TestSpecificEP(TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.prof_id = create_professional(uuid())
    
    def tearDown(self):
        del_user(self.prof_id)

    def test_EP_specific_insert_hour_incomplete(self):
        print(f' ERROR: Insert via /specifics hora incompleta \n S:10:00 E:12:30')


        data = {
            'start': '10:00',
            'end': '12:30',
            'day': '2025-03-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual( response.json(), {'detail': 'No es una hora completa'})

    def test_EP_specific_insert_hour_invalid(self):
        print(f' ERROR: Insert via /specifics hora incorrecta')
        print('End > Start')

        data = {
            'start': '13:00',
            'end': '10:00',
            'day': '2025-03-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Start > End incorrect'})
    
    def test_EP_specific_insert_E0_hour(self):
        print(f'Insert via /specifics hora End: 0')
        print('End == 0')

        data = {
            'start': '1:00',
            'end': '00:00',
            'day': '2025-03-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)
        test = jsonable_encoder({'start': time(hour=1),
            'end': time(hour=0),
            'day': date(year=2025, month=3, day=3),
            'prof_id': self.prof_id,
            'isCanceling': False})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_EP_specific_insert_S0E0_hour(self):
        print(f'Insert via /specifics hora start == end == 0')
        print('Start == End == 0')

        data = {
            'start': '0:00',
            'end': '00:00',
            'day': '2025-02-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)
        test = jsonable_encoder(
            {'start': time(hour=0),
            'end': time(hour=0),
            'day': date(year=2025, month=2, day=3),
            'prof_id': self.prof_id,
            'isCanceling': False})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)
        
    def test_EP_specific_get(self):
        month = 1
        print(f'Get Specific Month {month}')
        
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/specifics?month={month}')
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder({'start': time(hour=10),
            'end': time(hour=13),
            'day': date(year=2025, month=month, day=3),
            'prof_id': self.prof_id,
            'isCanceling': False})
        
        self.assertEqual(response.json(), {'specific': [test]})

    def test_EP_specific_get_void(self):
        year = 2023
        month = 1
        print(f'Get Specific Month {month} Year {year}')

        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/specifics?month={month}&year={year}')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.json(), {'specific': []})

    def test_EP_specific_get_invalid_month(self):
        month = 20
        print(f' ERROR: Get month= {month} Specific')

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/specifics?month={month}')
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.json(), {'detail':'Valor de mes invalido'})




    def test_EP_specific_update_None(self):
        print('ERROR: Update  None data')
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-01-02'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)
        update = {
            'start': '10:00',
            'day': '2025-02-03'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Not update'})

    def test_EP_specific_update_start(self):
        print('Update start')
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-02-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)   
        
        update = {
            'start': '10:00',
            'day': '2025-02-03',
            'Nstart': '03:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('03:00'),
            'day': '2025-02-03',
            'end': time.fromisoformat('13:00'),
            'prof_id': self.prof_id,
            'isCanceling': False
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_specific_update_end(self):
        print('Update end')
        data = {
            'start': '13:00',
            'end': '19:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)     
        update = {
            'start': '13:00',
            'day': '2025-01-03',
            'Nend': '23:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('13:00'),
            'day': '2025-01-03',
            'end': time.fromisoformat('23:00'),
            'prof_id': self.prof_id,
            'isCanceling': False
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_specific_update(self):
        print('Update Complete')
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-02-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        update = {
            'start': '10:00',
            'day': '2025-02-03',
            'Nend': '19:00',
            'Nstart': '15:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)

        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('15:00'),
            'day': '2025-02-03',
            'end': time.fromisoformat('19:00'),
            'prof_id': self.prof_id,
            'isCanceling': False
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_specific_update_not_complete(self):
        print('ERROR: Update Hour not complete')
        self.test_EP_specific_insert_S0E0_hour()
        update = {
            'start': '00:00',
            'day': '2025-02-03',
            'Nstart': '20:00',
            'Nend': '22:30'
            
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'No es una hora completa'})
    
    def test_EP_specific_update_not_valid(self):
        print('ERROR: Update start > end')
        self.test_EP_specific_insert_S0E0_hour()
        update = {
            'start': '00:00',
            'day': '2025-02-03',
            'Nstart': '22:00',
            'Nend': '20:00'
            
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Start > End incorrect'})

    def test_EP_specific_update_include(self):
        print('ERROR: Update include')
        data = {
            'start': '00:00',
            'end': '10:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        data = {
            'start': '15:00',
            'end': '19:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        update = {
            'start': '00:00',
            'day': '2025-01-03',
            'Nstart': '17:00',
            'Nend': '23:00'
        }

        response = self.client.put(f'/professionals/{self.prof_id}/agenda/specifics', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Time incluide'})

    def test_EP_specific_not_delete(self):
        print('ERROR: Delete Specific not exist')
        data = {'start':'10:20', 'day':'2025-05-02'}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/specifics', params=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail':'Day not found'})
    
    def test_EP_specific_delete(self):
        print('Delete Specific')
        data = {
            'start': '15:00',
            'end': '19:00',
            'day': '2025-05-02'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        data = {'start':'15:00', 'day':'2025-05-02'}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/specifics', params=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'detail':'Day deleted sucessfully'})

    def test_EP_specif_get_hours(self):
        print('Get hours from Day')
        data = {
            'start': time.fromisoformat('15:00'),
            'end': time.fromisoformat('19:00'),
            'day': '2025-05-02'
        }
        data = jsonable_encoder(data)
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/specifics', json= data)

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/specifics/day?day={data["day"]}')

        self.assertEqual(response.status_code, 200)
        data.update({'prof_id':self.prof_id, 'isCanceling':False})
        
        self.assertEqual(response.json(), {'specific': [data]})        