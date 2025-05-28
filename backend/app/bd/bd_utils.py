from datetime import time, timedelta
from pydantic import BaseModel


class MinuteError(Exception):
    msg = 'Minute Accept 00 or 30'

class Schedule(BaseModel):
    start:time
    end:time

class Errors(BaseModel):
    error: str

class Info(BaseModel):
    INFO: str


#Funcion que toma un tiempo, y solo acorta a hora y minutos (elimina segundos y TZ) retornando la modificacion
def strip_time_hour_minute(tiempo: time) -> time:
    hora = tiempo.hour
    minuto = tiempo.minute
    if minuto not in [00, 30]:
        raise MinuteError
    tiempo = time(hour=hora, minute=minuto)
    return tiempo

#Funcion que verifica si inicio >= fin
def valid_time(inicio:time, fin:time) -> bool:
    #si la hora de fin es la 0, reemplaza en fin la hora por 23:59
    if fin.hour == 0:
        fin = fin.replace(hour=23, minute=59)

    if inicio >= fin:
        return False
    else:
        return True
    
#Funcion que recibe una lista con horarios, el inicio y fin ingresados
def include_time(db_recurrent:list[Schedule], inicio: time, fin: time ) -> bool: 
    incluido = False
    #si inicio no es la 0 o las 23, reemplaza la hora de inicio por la hora siguiente
    if inicio.hour not in  [0, 23] :
        inicio = inicio.replace(hour=(inicio.hour + 1))
    #Si fin es distinto de las 0, resta una hora a el final
    if fin.hour != 0:
        fin = fin.replace(hour=(fin.hour -1))
    #Sino reemplaza la hora por 23:59
    else:
        fin = fin.replace(hour=23, minute=59)
    #recorre la lista de horas
    for dbr in db_recurrent:
        #almacena la hora de inicio que esta en la lista de objeto
        hora = dbr.start
        #lo agrega a una lista horas
        horas = [hora]
        #recorre hasta llegar al end del objeto
        while hora < dbr.end:
            hourP1 = hora.hour
            #suma una hora
            hourP1 += 1
            #crea el time con la hora cambiada
            hora = hora.replace(hour= hourP1)
            #lo agrega a la lista
            horas.append(hora)
        #comprueba si el inicio y el final no estan el la lista ["8:00","9:00","10:00",...]
        if inicio in horas and fin in horas:
            incluido = True
            break
    return incluido

   
def test_time(db_recurrent:list[Schedule], inicio: time, fin: time ) -> bool: 
    incluido = False

    inicioaux = timedelta(hours=inicio.hour, minutes=inicio.minute)
    finaux = timedelta(hours=fin.hour, minutes=fin.minute)

    if inicio.hour not in  [0, 23] :
        inicioaux = inicioaux + timedelta(minutes= 30)
        inicio = __conver_hour_minute(inicioaux)
        del inicioaux
    if fin.hour != 0:
        finaux = finaux - timedelta(minutes=30)
        fin = __conver_hour_minute(finaux)
        del finaux
    else:
        fin = fin.replace(hours=23, minutes=59)

    comp = __desglozar(inicio, fin)

    for dbr in db_recurrent:
        horas = __desglozar(dbr.start, dbr.end)
        
        for c in comp:
            if c in horas:
                incluido = True
                break
        if incluido:
            break
    return incluido

def test2_time(db_recurrent:list[Schedule], inicio: time, fin: time ) -> bool:
    incluido = False

    inicioaux = timedelta(hours=inicio.hour, minutes=inicio.minute)
    finaux = timedelta(hours=fin.hour, minutes=fin.minute)

    if inicio.hour not in  [0, 23] :
        inicioaux = inicioaux + timedelta(minutes= 30)
        inicio = __conver_hour_minute(inicioaux)
        del inicioaux
    if fin.hour != 0:
        finaux = finaux - timedelta(minutes=30)
        fin = __conver_hour_minute(finaux)
        del finaux
    else:
        fin = fin.replace(hours=23, minutes=59)
    
    for dbr in db_recurrent:
        if inicio < dbr.start or dbr.end > fin:
            incluido = True
            break
    return incluido


def error_hand(e:Exception):
    error = str(e.__cause__)
    ind = error.index("DETAIL")
    error = error[ind:]
    return error

def __conver_hour_minute(delta:timedelta) -> time:
    hor = delta.seconds // 3600
    minu = delta.seconds - (hor * 3600)
    minu = minu // 60
    hora = time(hor, minu)
    return hora

def __desglozar(inicio:time, fin:time) -> list[time]:
    min30 = timedelta(minutes=30)
    desglo = [inicio]
    hora = timedelta(hours=inicio.hour, minutes=inicio.minute)
    end = timedelta(hours=fin.hour, minutes=fin.minute)
    while hora < end:
        hora = hora + min30
        desglo.append(__conver_hour_minute(hora))
    return desglo

"""
from datetime import datetime, time, timedelta
dia = datetime.now()
print(f'{dia}')
print(f'{dia.isoweekday()}') #{1: "Lunes", 2:"Martes", ..., 7:"Domingo"}
inicio = time(hour=8,minute=00)
fin = time(hour=10,minute=00)
hora = inicio
horas = [inicio.isoformat()]
while hora < fin:
  h = hora.hour
  h +=1
  hora = hora.replace(hour=h)
  horas.append(hora.isoformat())
  

print(f'{inicio} {fin} {horas} {"09:00:00" in horas }')"""