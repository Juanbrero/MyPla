from datetime import time


#Funcion que toma un tiempo, y solo almacena hora y minutos (elimina segundos y TZ)
def strip_time_hour_minute(tiempo: time):
    hora = tiempo.hour
    minuto = tiempo.minute
    tiempo = time(hour=hora, minute=minuto)
    return tiempo