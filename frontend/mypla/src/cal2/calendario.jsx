import React, { useState, useEffect } from 'react';
import CeldaHora from './celdaHora.jsx';
import { prof_id } from "../utils/testData";
import { getAvailableProfessional, postSpecific, postRecurrent, deleteSpecific, deleteRecurrent, getProfessionalTopics } from './service.js';
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, setHours, setMinutes, weeksToDays} from 'date-fns';
import { es } from 'date-fns/locale';
import './calendario.css';
import ScheduleCreate from './crear';
import ScheduleEdit from './edit.jsx';

// --- CONST: horas del calendario ----------------------------------------------------------
const horasDelDia = Array.from({ length: 24 }, (_, i) => i + 0); // 0 a 23

// --- funciones utilitarias para hora ------------------------------------------------------
const parseHora = (horaStr) => {
    if (!horaStr) return '';
    return horaStr.slice(0, 5);
};

const horaNumero = (horaStr) => {
    if (!horaStr) return null;
    return parseInt(horaStr.slice(0, 2), 10);
};

const obtenerDiaDeLaSemana = (fecha) => {
  const [anio, mes, dia] = fecha.split('-');
  const date = new Date(Date.UTC(anio, mes - 1, dia));
  return date.getUTCDay();
};

const toISO8601 = (hora, minutos = '00') => {
  return `${String(hora).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:00.000Z`;
};

function getRawTimeString(date) {
  const horas = String(date.getHours()).padStart(2, '0');
  const minutos = String(date.getMinutes()).padStart(2, '0');
  const segundos = String(date.getSeconds()).padStart(2, '0');
  const milisegundos = String(date.getMilliseconds()).padStart(3, '0');
  return `${horas}:${minutos}:${segundos}.${milisegundos}Z`; // O sin la Z, según quieras
}

function formatTimeUndefined(inputTime, defaultMilliseconds = '000') {
  // 1. Limpiar el string de "undefinedT" si existe
  const cleanTime = inputTime.toString().replace('undefinedT', '');
  
  // 2. Extraer horas, minutos y segundos
  const timeParts = cleanTime.split(':');
  
  // 3. Validar y obtener componentes
  const hours = timeParts[0]?.padStart(2, '0') || '00';
  const minutes = timeParts[1]?.padStart(2, '0') || '00';
  const seconds = timeParts[2]?.split('.')[0]?.padStart(2, '0') || '00';
  
  // 4. Obtener milisegundos si existen, sino usar los predeterminados
  const milliseconds = timeParts[2]?.includes('.') 
    ? timeParts[2].split('.')[1]?.padEnd(3, '0').substring(0, 3) 
    : defaultMilliseconds;
  
  // 5. Construir el nuevo formato
  return `${hours}:${minutes}:${seconds}.${milliseconds}Z`;
}

// --- obtener los eventos de cada dia ------------------------------------------------------
const filtrarEventosPorDia = (eventos, dia) => {
     if (!eventos) return { recurrent: [], specific: [], exception: [] };

     const { recurrent = [], specific = [], exception = [] } = eventos;

    // Filtrar específicos para el día
    const especificosDelDia = specific.filter(e => isSameDay(parseISO(e.day), dia));

    // Filtrar excepciones para el día
    const excepcionesDelDia = exception.filter(e => isSameDay(parseISO(e.day), dia));

    // Filtrar recurrentes para el día, omitiendo los que tienen excepción y que coincidan con la hora
    const recurrentesDelDia = recurrent.filter(e => {
        const esElDia = getDay(dia) === e.week_day;
        const horaEv = horaNumero(parseHora(e.start));
        const tieneExcepcion = excepcionesDelDia.some(exc => {
            const horaInicioRecurrente = parseHora(e.start);
            const horaInicioExcepcion = parseHora(exc.start);
            return esElDia && horaInicioRecurrente === horaInicioExcepcion;
        });
        return esElDia && !tieneExcepcion;
    });

    return {
        recurrent: recurrentesDelDia,
        specific: especificosDelDia,
        exception: excepcionesDelDia,
    };
};

const Calendario = () => {

    // estados modal crear
    const [createModalOpen, setCreateModalOpen] = useState(false);
    const [createModalData, setCreateModalData] = useState(null); // Datos que le paso al modal

    // estados modal edit
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [editModalData, setEditModalData] = useState(null);

    // dia de inicio de la semana 
    const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));

    const [eventos, setEventos] = useState({});
    const [professionalTopics, setProfessionalTopics] = useState({});

    // --- hago click en una celda ---------------------------------------------------------------
    const handleCeldaClick = (dia, hora, evento = null) => {
        // Abrir modal de EDITAR si hay evento
        if (evento) {
            const updatedEvento = {
                ...evento,          
                start_actual: evento.start, 
                day_actual: evento.day
            };
            setEditModalData(updatedEvento);
            setEditModalOpen(true);
        }
        // Abrir modal de CREAR si no hay evento
        else {
            const diaStr = format(dia, 'yyyy-MM-dd')
            setCreateModalData({
                start: toISO8601(hora),
                end: toISO8601(hora + 1),
                topics: [],
                avaliableTopics: professionalTopics,
                day: diaStr,
                week_day: obtenerDiaDeLaSemana(diaStr),
                recurrent: false,
            });
            setCreateModalOpen(true);
        }
    };

    // --- cierro el (modal de CREATE) --------------------------------------------------------------
    const handleCloseCreateModal = () => {
        setCreateModalOpen(false);
        setCreateModalData(null);
    };

    // --- cierro el (modal de EDIT) --------------------------------------------------------------
    const handleCloseEditModal = () => {
        setEditModalOpen(false);
        setEditModalData(null);
    };

    // --- guardo nueva tarea (modal de CREATE) ---------------------------------------------------
    const handleSaveNewTask = async (newTask) => {
      let data = {}
      try {
        if (newTask.category == 'recurrent') {
          data = {
            week_day: new Date(newTask.day).getDay() + 1,
            start: typeof newTask.start === 'string' ? formatTimeUndefined(newTask.start) : getRawTimeString(newTask.start),
            end: typeof newTask.end === 'string' ? formatTimeUndefined(newTask.end) : getRawTimeString(newTask.end),
            topics: newTask.topics
          }
          await postRecurrent(prof_id, data)
        }
        else {
          data = {
            day: newTask.day,
            start: typeof newTask.start === 'string' ? formatTimeUndefined(newTask.start) : getRawTimeString(newTask.start),
            end: typeof newTask.end === 'string' ? formatTimeUndefined(newTask.end) : getRawTimeString(newTask.end),
            topics: newTask.topics
          }
          await postSpecific(prof_id, data)
        }

        setCreateModalOpen(false);
        setCreateModalData(null);

        await cargarEventos(prof_id);
      } catch (error) {
        console.error('Error al guardar la tarea:', error);
      }
    };


    // --- edito una tarea (modal de EDIT) --------------------------------------------------------
    const handleSaveEditTask = (updatedEvent) => {
      // console.log(updatedEvent)
      // let data = {}
      // if (updatedEvent.type == 'recurrent') {
        
      // }
      // else {
      //   data = {
      //     day: updatedEvent.day_actual,
      //     start: formatTimeUndefined(updatedEvent.start_actual),
      //     Nday: formatTimeUndefined(updatedEvent.day),
      //     Nstart: formatTimeUndefined(updatedEvent.start),
      //     Nend: formatTimeUndefined(updatedEvent.end),
      //     topics: updatedEvent.topics
      //   }
      //   console.log(data)
      // }

        // TODO : guardar en back y recargar



            // setEventos((prev) => {
            //    const tipo = updatedEvent.extendedProps?.category === 'recurrent' ? 'recurrent' : 'specific';

            //     const actualizados = prev[tipo].map((ev) =>
            //         ev.id === updatedEvent.id ? { ...ev, ...updatedEvent } : ev
            //     );

            //     return { ...prev, [tipo]: actualizados };
            // });
            // handleCloseEditModal();
    };

    // --- borro una tarea (modal de EDIT) --------------------------------------------------------
    const handleDeleteTask = async (eventToDelete) => {
      let data = {}
      try {
        if (eventToDelete.type == 'recurrent') {
          const week_day = eventToDelete.week_day
          const start = formatTimeUndefined(eventToDelete.start)
          await deleteRecurrent(prof_id, week_day, start)
        }
        else if (eventToDelete.type == 'specific') {
          data = {
            day: eventToDelete.day,
            start: formatTimeUndefined(eventToDelete.start)
          }
          await deleteSpecific(prof_id, data)
        }

        setCreateModalOpen(false);
        setCreateModalData(null);

        await cargarEventos(prof_id);
      } catch (error) {
        console.error('Error al guardar la tarea:', error);
      }

        
            // setEventos((prev) => {
            //     const tipo = eventToDelete.extendedProps?.category === 'recurrent' ? 'recurrent' : 'specific';

            //     const filtrados = prev[tipo].filter((ev) => ev.id !== eventToDelete.id);

            //     return { ...prev, [tipo]: filtrados };
            // });

            // handleCloseEditModal();
    };

    // --- cancelo tarea por unica vez (modal de EDIT) --------------------------------------------
    const handleCancelOneOccurrence = (eventToCancel) => {

        // TODO : guardar en back y recargar

            // console.log("Cancelar solo una ocurrencia:", eventToCancel);
            // // Aquí decides: ¿creas una "excepción"? ¿O lo eliminas de la vista?
            // // Ejemplo sencillo: lo eliminamos visualmente:
            // setEventos((prev) => {
            //     const tipo = 'specific'; // Lo tratarías como evento específico a partir de ahora
            //     const nuevos = [...prev[tipo], { ...eventToCancel, cancelled: true }];
            //     return { ...prev, [tipo]: nuevos };
            // });

            // handleCloseEditModal();
    };

    // --- cargo los EVENTOS de la base de datos --------------------------------------------------
    const cargarEventos = async (profId) => {
        try {
            const data = await getAvailableProfessional(profId);
            setEventos(data);
            const topics = await getProfessionalTopics(profId);
            setProfessionalTopics(topics);
        } catch (error) {
            console.error("Error cargando eventos:", error);
        }
    };
    useEffect(() => {
        cargarEventos(prof_id);
    }, [semanaInicio]);

    const siguienteSemana = () => setSemanaInicio(addDays(semanaInicio, 7));
    const anteriorSemana = () => setSemanaInicio(addDays(semanaInicio, -7));

    const diasSemana = Array.from({ length: 7 }).map((_, i) => addDays(semanaInicio, i));

    // obtengo los eventos en cada dia que se muestra en la agenda
    const eventosPorDia = diasSemana.reduce((acc, dia) => {
        acc[format(dia, 'yyyy-MM-dd')] = filtrarEventosPorDia(eventos, dia);
        return acc;
    }, {});

    return (
    <div className="p-4 calendario">
      <div className="calendario-controles">
        <button className="direccion" onClick={anteriorSemana}>⬅️ Anterior</button>
        <h2 className="text-xl font-bold">{format(semanaInicio, "'Semana de' dd/MM/yyyy")}</h2>
        <button className="direccion" onClick={siguienteSemana}>Siguiente ➡️</button>
      </div>

      <div className="calendario-contenedor">
        <div className="columna-horas">
          <div className="header-horas"></div>
          {horasDelDia.map(hora => (
            <div key={hora} className="hora">{hora}:00</div>
          ))}
        </div>

        <div className="grid-dias">
          {diasSemana.map((dia, idxDia) => (
            <div key={`header-${idxDia}`} className="header-dia">
              {format(dia, 'EEE dd/MM', {locale: es})}
            </div>
          ))}

          {horasDelDia.map(hora =>
            diasSemana.map((dia, idxDia) => {
              const keyDia = format(dia, 'yyyy-MM-dd');
              const eventosDelDia = eventosPorDia[keyDia];

              return (
                <CeldaHora
                  key={`${hora}-${idxDia}`}
                  dia={dia}
                  hora={hora}
                  eventosDelDia={eventosDelDia}
                  onClick={handleCeldaClick}
                />
              );
            })
          )}
        </div>
      </div>

      <ScheduleCreate
          open={createModalOpen}
          onClose={handleCloseCreateModal}
          taskData={createModalData}
          onCancelTask={handleCloseCreateModal}
          onSaveTask={handleSaveNewTask}
      />


      <ScheduleEdit
          open={editModalOpen}
          onClose={handleCloseEditModal}
          clickedEvent={editModalData}
          taskData={editModalData}
          onCancelTask={handleCloseEditModal}
          onSaveEditTask={handleSaveEditTask}
          onDeleteTask={handleDeleteTask}
          onCancelOneOccurrence={handleCancelOneOccurrence}
      />

    </div>
  );
};

export default Calendario;
