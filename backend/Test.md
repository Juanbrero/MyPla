# Testing
Utilizar pytest y unittest
> 📌 **Importante:** 
> 
> Siempre ejecutar desde **/backend**
~~~
(.venv)/backend$ pytest 
~~~
Se ejecutaran desde backend todo file llamado test_* que contenga una funcion test_*.
Ejecutar un archivo o función especifica
> 💡 **Consejo:** 
>
> Se recomienda utilizar los metodos de aqui debajo para limitar la ejecución de los test, y no ejecutar todos los creados
~~~
(.venv)/backend$ pytest path/to/test_*py
(.venv)/backend$ pytest path/to/test_*py::[CLASS]::[FUNCTION]
~~~
| Test | Link |
|-  |   -   |
| [Recurrent](#recurrent)| |
| | [Insert](#insert-recurrent) |
| | [Get](#get-recurrent) |
| | [Update](#update-recurrent) |
| | [Delete](#delete-recurrent) |
|[Specific](#specific)| |
||[Insert](#insert-specific) | 
|[Reservation](#reservation)| |
|[Class](#class-reservation)| |

## Recurrent
### Insert Recurrent
 - [ ]  Caso existos -> 201
   - [x]  Repository
   - [ ]  Endpoint
---
 - [ ] Week invalido -> 400
   - [x]  Repository
   - [ ]  Endpoint
---
 - [ ] Hora invalida(not 00 or 30) 13:25  -> 406

   - [ ] Inicio
     - [x]  Repository
     - [ ]  Endpoint

   - [ ] Fin
     - [x]  Repository
     - [ ]  Endpoint
---
 - [ ] Horario incompleta 10:00-12:30 | 12:30-15:00 -> 400
    
   - [ ] Inicio
     - [x]  Repository
     - [ ]  Endpoint

   - [ ] Fin
     - [x]  Repository
     - [ ]  Endpoint
---
 - [ ] Week and horario error  -> 400
     - [x]  Repository
     - [ ]  Endpoint
---
 - [x] Horario invalida 16:30-12:30
    - [x]  Repository
    - [ ]  Endpoint
---
 - [ ] Time include
    - [x]  Repository
    - [ ]  Endpoint
---
 - [ ] Hora de fin 00
    - [x]  Repository
    - [ ]  Endpoint
---
 - [ ] Topics
   - [ ] Topico valido
      - [X]  Repository
      - [ ]  Endpoint

   - [ ] Topicos validos
      - [X]  Repository
      - [ ]  Endpoint

   - [ ] Topico inexistente
      - [X]  Repository
      - [ ]  Endpoint

   - [ ] Topico no perteneciente
      - [X]  Repository
      - [ ]  Endpoint

---

### Get Recurrent
- [ ] Recuperar un dia de la semana (week)
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Recuperar un dia de la semana sin horarios (week)
  - [X]  Repository
  - [ ]  Endpoint
---
- [ ] Recuperar un dia de la semana invalido (week != [1-7])
  - [X]  Repository
  - [ ]  Endpoint
---
- [ ] Topics
  - [ ] Recuperar todos los topicos de un recurrente
    - [X]  Repository
    - [ ]  Endpoint

--- 
### Update Recurrent
- [ ] Actualizar sin enviar datos (llamada vacia)
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con hora invalida (Minute != 00/30)
  - [X]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con horarios invalido (Start > End)
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar inicio
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar fin
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar sin horarios (vacio)
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con horarios colisionantes
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con semana invalida
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar completo
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Topicos
  
  - [ ] Agregar Topico valido
    - [X]  Repository
    - [ ]  Endpoint
  
  - [ ] Agregar topico Invalido
    - [X]  Repository
    - [ ]  Endpoint
  
  - [ ] Eliminar topico valido
    - [X]  Repository
    - [ ]  Endpoint
  
  - [ ] Eliminar topico invalido
    - [ ]  Repository
    - [ ]  Endpoint
  
  - [ ] Eliminar último topico
    - [X]  Repository
    - [ ]  Endpoint

### Delete Recurrent

- [ ] Eliminar Horario valido
    - [x]  Repository
    - [ ]  Endpoint
---
- [ ] Eliminar semana Invalido
    - [X]  Repository
    - [ ]  Endpoint



## Specific
### Insert Specific
- [x] Caso exitoso

## Reservation
### Class Reservation
- [ ] Caso exitoso
