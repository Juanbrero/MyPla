from fastapi.testclient import TestClient
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from uuid import uuid4 as uuid

from datetime import date, time

from app.main import app
from app.bd.schemas import schema_exception
from app.config.database import get_db
from app.repository.exception_repository import ExceptionRepository
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

class TestExceptionRepository(TestCase):

    
    def setUp(self):
        self.prof_id = create_professional(uuid())
        self.db = get_db_repository()
        self.excepcion_repository = ExceptionRepository(self.db)

    def tearDown(self):
        del_user(self.prof_id)
        
    def test_excepcion_insert(self):
        """
        Se crea una excepción
        """
        print('Insertar un excepción')
        
        excepcion = schema_exception.ExceptionCreate( day=date(year=2025, month=1, day=23),
                                                            start=time(hour=10),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_excep_create = self.excepcion_repository.create(excepcion)
        self.assertEqual(obj_excep_create.prof_id, self.prof_id)
        self.assertEqual( obj_excep_create.isCanceling, True) 
        

    def test_excepcion_get_complete(self):
        """
        Recupera un dia Excepcion, pasando todos su PK
        """
        
        print('Get Excepcion Day')
        
        excepcion = schema_exception.ExceptionCreate( day=date(year=2025,month=1,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_excepcion_create = self.excepcion_repository.create(excepcion)

        obj_excep_get = self.excepcion_repository.get_day(excepcion)
        dict_excep_test = schema_exception.ExceptionGet.from_orm(obj_excep_get)

        test_json = jsonable_encoder({
            'day': date(year=2025,month=1,day=23),
            'start':time(hour=9),
            'end': time(hour=12)
        })

        self.assertEqual( jsonable_encoder(dict_excep_test), test_json)

    
    def test_excepcion_get_month(self):
        """
        Recupera todos los dias excepcion de un mes particular
            - prof_id
            - month
        Anio, se considera como actual
        """
        

        print('Get Exception Day from Month')
        

        excepcion = schema_exception.ExceptionCreate( day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_excep_create = self.excepcion_repository.create(excepcion)
       
        excepcion_MY = schema_exception.ExceptionMonthYear(prof_id= self.prof_id,
                                                                month= 6)
        
        list_obj_excep_get = self.excepcion_repository.get_month_year(excepcion_MY)
        test = [{
            'day': date(year=2025,month=1,day=23),
            'start':time(hour=9),
            'end': time(hour=12)
        }]
        self.assertGreater(len(list_obj_excep_get), 0)

        for spec in range(len(list_obj_excep_get) - 1):
            spec_test = schema_exception.ExceptionGet.from_orm(spec_test[spec])
            test_value = test[spec]
            self.assertEqual( jsonable_encoder(spec_test), jsonable_encoder(test_value))



    def test_excepcion_not_year(self):
        """
        Error de buscar dias excepcionales con un año inexistente
        """
        
        print('Get Exception Day from Not exist Year')
               
        
        excepcion_MY = schema_exception.ExceptionMonthYear(prof_id= self.prof_id,
                                                                month= 6,
                                                                year= 2024)

        list_excep_get = self.excepcion_repository.get_month_year(excepcion_MY)

        self.assertEqual(len(list_excep_get), 0)
       

    def test_excepcion_start_update(self):
        """
        Actualizar hora de inicio
        """
        
        print('Update Exception start')
        
        
        excepcion_insert = schema_exception.ExceptionCreate( day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_excep_create = self.excepcion_repository.create(excepcion_insert)
       

        obj_excep_get = self.excepcion_repository.get_day(excepcion_insert)
        

        excep_update = schema_exception.ExceptionGet(day=date(year=2025,month=6,day=23),
                                                            start=time(hour=7),
                                                            end= time(hour=12))
        

        excepcion_update = self.excepcion_repository.update(obj_excep_get, excep_update)


        excep_test = schema_exception.ExceptionGet.from_orm(excepcion_update)
        excep_test = jsonable_encoder(excep_test)
        
        dict_excep_update = jsonable_encoder(excep_update)
        self.assertEqual( excep_test, dict_excep_update)


    def test_excepcion_end_update(self):
        """
        Actualizar hora de fin
        """
        
        print('Update Exception End')
        
        
        excepcion_insert = schema_exception.ExceptionCreate( day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        
        obj_excep_create = self.excepcion_repository.create(excepcion_insert)
       

        obj_excep_get = self.excepcion_repository.get_day(excepcion_insert)


        excep_update = schema_exception.ExceptionGet(day=date(year=2025,month=6,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=23))
        

        excepcion_update = self.excepcion_repository.update(obj_excep_get, excep_update)


        spec_test = schema_exception.ExceptionGet.from_orm(excepcion_update)
        spec_test = jsonable_encoder(spec_test)
        
        dict_excep_update = jsonable_encoder(excep_update)
        self.assertEqual( spec_test, dict_excep_update)


    def test_excepcion_update(self):
            """
            Actualizar hora de inicio y fin
            """
            db = get_db_repository()
            
            print('Update Exception Hour')
            
            
            excepcion_insert = schema_exception.ExceptionCreate( day=date(year=2025,month=6,day=23),
                                                                start=time(hour=8),
                                                                end= time(hour=13),
                                                                prof_id= self.prof_id
                                                                )
            
            obj_excep_create = self.excepcion_repository.create(excepcion_insert)
        

            obj_excep_get = self.excepcion_repository.get_day(excepcion_insert)
    
            excep_update = schema_exception.ExceptionGet(day=date(year=2025,month=6,day=23),
                                                                start=time(hour=6),
                                                                end= time(hour=22))
           

            excepcion_update = self.excepcion_repository.update(obj_excep_get, excep_update)


            spec_test = schema_exception.ExceptionGet.from_orm(excepcion_update)
            spec_test = jsonable_encoder(spec_test)
            dict_excep_update = jsonable_encoder(excep_update)

            self.assertEqual( spec_test, dict_excep_update)


    def test_excepcion_delete(self):
        
        print('Delete Excepcion')
        
        excepcion_insert = schema_exception.ExceptionCreate( day=date(year=2024,month=7,day=8),
                                                            start=time(hour=15),
                                                            end= time(hour=20),
                                                            prof_id= self.prof_id
                                                            )
        

        excep_create = self.excepcion_repository.create(excepcion_insert)
       

        obj_excep_get = self.excepcion_repository.get_day(excepcion_insert)

        spec_delete = self.excepcion_repository.delete(obj_excep_get)
        
        self.assertTrue (spec_delete, excepcion_insert)
    
    def test_isInclude(self):
        print('Is Include')
        excepcion = schema_exception.ExceptionCreate( day=date(year=2025,month=1,day=1),
                                                            start=time(hour=10),
                                                            end= time(hour=18),
                                                            prof_id= self.prof_id
                                                            )
       
        self.excepcion_repository.create(excepcion)
        excepcion.start = time(hour=19)
        excepcion.end = time(hour=21)

        self.excepcion_repository.create(excepcion)

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
        
        test = [True, False, False, True, True, True, True, True, True]

        dict_excepcion = excepcion.dict()
        for tim in range(len(times)):
            dict_excepcion.update(times[tim])

            include = schema_exception.ExceptionCreate(**dict_excepcion)
            isInclude = self.excepcion_repository.isInclude(include)
            self.assertEqual(isInclude, test[tim], dict_excepcion)
            
    def test_isValid(self):
        print('Is Valid')
        test = [True, False, True]
        values = [{'start': time.fromisoformat('00:00'), 'end': time.fromisoformat('00:00')},
                  {'start': time.fromisoformat('10:00'), 'end': time.fromisoformat('09:00')},
                  {'start': time.fromisoformat('00:00'), 'end': time.fromisoformat('09:00')}]
        for v in range(len(values) - 1):
            response = self.excepcion_repository.isValidTime(values[v]['start'],values[v]['end'])
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
            response = self.excepcion_repository.isCompleteHour(tiempo[hora]['start'], tiempo[hora]['end'])
            self.assertTrue(response, tiempo[hora])
        for hora in range(5,10):
            response = self.excepcion_repository.isCompleteHour(tiempo[hora]['start'], tiempo[hora]['end'])
            self.assertFalse(response, tiempo[hora])

    def test_trunc_time(self):
        test = self.excepcion_repository.trunc_time(time.fromisoformat('20:01:23'))
        self.assertEqual(test, time.fromisoformat('20:01'))

    def test_exception_get_hours(self):
        print('Get hours from one day')
        excepcion = schema_exception.ExceptionCreate( day=date(year=2025,month=9,day=23),
                                                            start=time(hour=9),
                                                            end= time(hour=12),
                                                            prof_id= self.prof_id
                                                            )
        obj_excep_create = self.excepcion_repository.create(excepcion)

        excep_get = schema_exception.ExceptionGetDat(day=excepcion.day, prof_id= excepcion.prof_id)
        list_hours = self.excepcion_repository.get_day_hours(excep_get)
        dict_test = excepcion.dict()
        dict_test.pop('prof_id')
        list(dict_test)
        for spec in range(len(list_hours) -1):
            excep_dict = schema_exception.ExceptionGet.from_orm(list_hours[spec])
            test_value = dict_test[spec]
            self.assertAlmostEqual(excep_dict, test_value)  


class TestExceptionEP(TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.prof_id = create_professional(uuid())
    
    def tearDown(self):
        del_user(self.prof_id)

    def test_EP_insert_hour_incomplete(self):
        print(f' ERROR: Insert via /exceptions hora incompleta \n S:10:00 E:12:30')


        data = {
            'start': '10:00',
            'end': '12:30',
            'day': '2025-03-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual( response.json(), {'detail': 'No es una hora completa'})

    def test_EP_exception_insert_hour_invalid(self):
        print(f' ERROR: Insert via /exceptions hora incorrecta')
        print('End > Start')

        data = {
            'start': '13:00',
            'end': '10:00',
            'day': '2025-03-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Start > End incorrect'})
    
    def test_EP_exception_insert_E0_hour(self):
        print(f'Insert via /exceptions hora End: 0')
        print('End == 0')

        data = {
            'start': '1:00',
            'end': '00:00',
            'day': '2025-03-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)
        test = jsonable_encoder({'start': time(hour=1),
            'end': time(hour=0),
            'day': date(year=2025, month=3, day=3)})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_EP_exception_insert_S0E0_hour(self):
        print(f'Insert via /exceptions hora start == end == 0')
        print('Start == End == 0')

        data = {
            'start': '0:00',
            'end': '00:00',
            'day': '2025-02-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)
        test = jsonable_encoder(
            {'start': time(hour=0),
            'end': time(hour=0),
            'day': date(year=2025, month=2, day=3)})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test)

    def test_EP_exception_get_hours(self):
        print('Get hours from Day')
        data = {
            'start': time.fromisoformat('15:00'),
            'end': time.fromisoformat('19:00'),
            'day': '2025-05-02'
        }
        data = jsonable_encoder(data)
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/exceptions/day?day={data["day"]}')

        self.assertEqual(response.status_code, 200)
        data.update({
            'isCanceling':True,
            'prof_id': self.prof_id})
        self.assertEqual(response.json(), {'exception': [data]})

    def test_EP_exception_get(self):
        month = 1
        print(f'Get Except Month {month}')
        
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/exceptions?month={month}')
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder({'start': time(hour=10),
            'end': time(hour=13),
            'day': date(year=2025, month=month, day=3),
            'isCanceling':True,
            'prof_id': self.prof_id})
        self.assertEqual(response.json(), {'exception': [test]})

    def test_EP_exception_get_void(self):
        year = 2023
        month = 1
        print(f'Get Exception Month {month} Year {year}')

        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/exceptions?month={month}&year={year}')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.json(), {'exception': []})

    def test_EP_exception_get_invalid_month(self):
        month = 20
        print(f' ERROR: Get month= {month} Exception')

        response = self.client.get(f'/professionals/{self.prof_id}/agenda/exceptions?month={month}')
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.json(), {'detail':'Valor de mes invalido'})


    def test_EP_exception_update_None(self):
            print('ERROR: Update  None data')
            data = {
                'start': '10:00',
                'end': '13:00',
                'day': '2025-01-02'
            }
            response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)
            update = {
                'start': '10:00',
                'day': '2025-02-03'
            }
            response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {'detail':'Not update'})

    def test_EP_exception_update_start(self):
        print('Update start')
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-02-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)   
        
        update = {
            'start': '10:00',
            'day': '2025-02-03',
            'Nstart': '03:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('03:00'),
            'day': '2025-02-03',
            'end': time.fromisoformat('13:00'),
            'prof_id': self.prof_id,
            'isCanceling': True
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_exception_update_end(self):
        print('Update end')
        data = {
            'start': '13:00',
            'end': '19:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)     
        update = {
            'start': '13:00',
            'day': '2025-01-03',
            'Nend': '23:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)
        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('13:00'),
            'day': '2025-01-03',
            'end': time.fromisoformat('23:00'),
            'prof_id': self.prof_id,
            'isCanceling': True
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_exception_update(self):
        print('Update Complete')
        data = {
            'start': '10:00',
            'end': '13:00',
            'day': '2025-02-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        update = {
            'start': '10:00',
            'day': '2025-02-03',
            'Nend': '19:00',
            'Nstart': '15:00'
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)

        self.assertEqual(response.status_code, 200)
        test = jsonable_encoder(
            {
            'start': time.fromisoformat('15:00'),
            'day': '2025-02-03',
            'end': time.fromisoformat('19:00'),
            'prof_id': self.prof_id,
            'isCanceling': True
            }
        )
        self.assertEqual(response.json(), test)

    def test_EP_exception_update_not_complete(self):
        print('ERROR: Update Hour not complete')
        self.test_EP_exception_insert_S0E0_hour()
        update = {
            'start': '00:00',
            'day': '2025-02-03',
            'Nstart': '20:00',
            'Nend': '22:30'
            
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'No es una hora completa'})
    
    def test_EP_exception_update_not_valid(self):
        print('ERROR: Update start > end')
        self.test_EP_exception_insert_S0E0_hour()
        update = {
            'start': '00:00',
            'day': '2025-02-03',
            'Nstart': '22:00',
            'Nend': '20:00'
            
        }
        response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Start > End incorrect'})

    def test_EP_exception_update_include(self):
        print('ERROR: Update include')
        data = {
            'start': '00:00',
            'end': '10:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        data = {
            'start': '15:00',
            'end': '19:00',
            'day': '2025-01-03'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        update = {
            'start': '00:00',
            'day': '2025-01-03',
            'Nstart': '17:00',
            'Nend': '23:00'
        }

        response = self.client.put(f'/professionals/{self.prof_id}/agenda/exceptions', json=update)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail':'Time incluide'})    

    def test_EP_exception_not_delete(self):
        print('ERROR: Delete Specific not exist')
        data = {'start':'10:20', 'day':'2025-05-02'}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/exceptions', params=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail':'Day not found'})
    
    def test_EP_exception_delete(self):
        print('Delete Specific')
        data = {
            'start': '15:00',
            'end': '19:00',
            'day': '2025-05-02'
        }
        response =  self.client.post(f'/professionals/{self.prof_id}/agenda/exceptions', json= data)

        data = {'start':'15:00', 'day':'2025-05-02'}
        response = self.client.delete(f'/professionals/{self.prof_id}/agenda/exceptions', params=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'detail':'Day deleted sucessfully'})
