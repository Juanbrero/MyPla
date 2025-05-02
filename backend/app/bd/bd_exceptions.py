class MinuteError(Exception):
    def __init__(self, minuto, msg='Los minutos deben ser "00" o "30" '):
        self.minuto = minuto
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f"Error el valor de minutos es {self.minuto} -> {self.msg}"

class CompleteHour(Exception):
    def __init__(self, mini, minf, msg='Las horas deben ser completas'):
        self.mini = mini
        self.minf = minf
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f"Error los minutos ingresados no son iguales {self.mini} != {self.minf} {self.msg}"
    
class WeekError(Exception):
    def __init__(self, week_day, msg='Valor no admitido'):
        self.week_day=week_day
        self.msg = msg
        super().__init__(self, msg)

    def __str__(self):
        return f'Dia de la semana fuera de rango (1..7) -> {self.week_day} '