from datetime import time, timedelta
from pydantic import BaseModel


class MinuteError(Exception):
    msg = 'Minute Accept 00 or 30'

class Schedule(BaseModel):
    start:time
    end:time

class Errors(BaseModel):
    error: str


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
def incluide_time(db_recurrent:list[Schedule], inicio: time, fin: time ) -> bool: 
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