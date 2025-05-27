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
Orden de evaluación
  - week
  - topic
  - hour
  - schedule
  - include
  - professional topics

### Insert Recurrent
 - [ ]  Caso existos -> 201
   - [x]  Repository
   - [x]  Endpoint
---
 - [ ] Week invalido -> 400
   - [x]  Repository
   - [x]  Endpoint
---
 - [ ] Hora invalida(not 00 or 30) 13:25  -> 406

   - [ ] Inicio
     - [x]  Repository
     - [x]  Endpoint

   - [ ] Fin
     - [x]  Repository
     - [x]  Endpoint
---
 - [ ] Horario incompleta 10:00-12:30 | 12:30-15:00 -> 400
    
   - [ ] Inicio
     - [x]  Repository
     - [x]  Endpoint

   - [ ] Fin
     - [x]  Repository
     - [x]  Endpoint
---
 - [ ] Week and horario error  -> 400
     - [x]  Repository
     - [x]  Endpoint
---
 - [x] Horario invalida 16:30-12:30 -> 400
    - [x]  Repository
    - [x]  Endpoint
---
 - [ ] Time include -> 400
    - [x]  Repository
    - [x]  Endpoint
---
 - [ ] Hora de fin 00 -> 201
    - [x]  Repository
    - [x]  Endpoint
---
 - [ ] Topics
   - [ ] Topico valido -> 201
      - [X]  Repository
      - [x]  Endpoint

   - [ ] Topicos validos -> 201
      - [x]  Repository
      - [x]  Endpoint

   - [ ] Topico inexistente -> 404
      - [X]  Repository
      - [x]  Endpoint

   - [ ] Topico no perteneciente -> 404
      - [X]  Repository
      - [x]  Endpoint

    - [ ] Topics vacio -> 400 
      - [X]  Repository
      - [x]  Endpoint

---

### Get Recurrent
- [ ] Recuperar un dia de la semana (week) -> 200
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Recuperar un dia de la semana sin horarios (week) -> 200 -> []
  - [X]  Repository
  - [ ]  Endpoint
---
- [ ] Recuperar un dia de la semana invalido (week != [1-7]) -> 400
  - [X]  Repository
  - [ ]  Endpoint
---
- [ ] Topics
  - [ ] Recuperar todos los topicos de un recurrente -> 200
    - [X]  Repository
    - [ ]  Endpoint

--- 
### Update Recurrent
- [ ] Actualizar sin enviar datos (llamada vacia) -> 400
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con hora invalida (Minute != 00/30) -> 406
  - [X]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con horarios invalido (Start > End) -> 400
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar inicio -> 200
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar fin -> 200
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar sin horarios (no existe) -> 404
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con horarios colisionantes -> 400
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar con semana invalida -> 400
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar completo -> 200
  - [x]  Repository
  - [ ]  Endpoint
---
- [ ] Actualizar sin cambio de horario -> 200
---
- [ ] Topicos
  
  - [ ] Agregar Topico valido -> 200
    - [X]  Repository
    - [ ]  Endpoint
  
  - [ ] Agregar topico Invalido -> 404
    - [X]  Repository
    - [ ]  Endpoint
  
  - [ ] Eliminar topico valido -> 200 
    - [X]  Repository
    - [ ]  Endpoint
  
  - [ ] Eliminar topico invalido ->
    - [ ]  Repository
    - [ ]  Endpoint
  
  - [ ] Eliminar último topico ->
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
