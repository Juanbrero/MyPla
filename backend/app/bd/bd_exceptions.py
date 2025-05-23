class MinuteError(Exception):
    """
    Error que se lanzara si los minutos no son los admitidos 
    """
    def __init__(self, minuto, msg='Los minutos deben ser "00" o "30" '):
        self.minuto = minuto
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f"Error minute value not equal {self.minuto} {self.msg}"

class CompleteHour(Exception):
    """
    Error que se lanzara si los minutos no son iguales, es decir, la hora no es completa
    """
    def __init__(self, mini, minf, msg='Las horas deben ser completas'):
        self.mini = mini
        self.minf = minf
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f"Error: Minute value of start and end not equal {self.mini} != {self.minf} {self.msg}"
    
class WeekError(Exception):
    """
    Error que se lanzara si el valor de week no esta en el rango aceptado
    """
    def __init__(self, week_day, msg='Valor no admitido'):
        self.week_day=week_day
        self.msg = msg
        super().__init__(self, msg)

    def __str__(self):
        return f'Week day is out of range (1..7) -> {self.week_day} '