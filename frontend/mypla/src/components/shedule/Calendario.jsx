import React, { useState, useEffect } from 'react';
import CeldaHora from './CeldaHora.jsx';
import { prof_id } from "../../utils/testData.js";
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, setHours, setMinutes, weeksToDays} from 'date-fns';
import { es } from 'date-fns/locale';
import './calendario.css';
import ScheduleCreate from './ScheduleModal.jsx';
import { getAvailableProfessional } from '../../services/available/available-professional.service.js';
import { postSpecific, putSpecific, deleteSpecific } from '../../services/specific/specific.service';
import { postRecurrent, putRecurrent, deleteRecurrent } from '../../services/recurrent/recurrent.service';
import { postException, putException, deleteException } from '../../services/exception/exception.service';
import { getProfessionalTopics } from '../../services/professionals-topic/professionals-topic.service.js';

// --- CONST: horas del calendario ----------------------------------------------------------
const horasDelDia = Array.from({ length: 24 }, (_, i) => i + 0); // 0 a 23

// --- funciones utilitarias para fechas y horas --------------------------------------------
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
        const esElDia = getDay(dia) === e.week_day % 7;
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
    // estados del modal
    const [createModalOpen, setCreateModalOpen] = useState(false);
    const [createModalData, setCreateModalData] = useState(null); 
    const [createModalMode, setCreateModalMode] = useState('create') // 'create', 'edit'

    // dia de inicio de la semana 
    const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));

    // datos de la bd
    const [eventos, setEventos] = useState({});
    const [professionalTopics, setProfessionalTopics] = useState({});

    // --- hago click en una celda ---------------------------------------------------------------
    const handleCeldaClick = (dia, hora, evento = null) => {
        // Abrir modal en EDITAR si hay evento
        const diaStr = format(dia, 'yyyy-MM-dd')
        if (evento) {
            setCreateModalData({
                start: `${evento.start}.000Z`,
                end: `${evento.end}.000Z`,
                topics: evento.topics,
                avaliableTopics: professionalTopics,
                day: evento.day ? evento.day : diaStr, //si es recurrente envio el dia en que se clickea para la generacion de excepciones
                week_day: evento.week_day % 7,
                recurrent: evento.type === 'recurrent',
                selectedHour: toISO8601(hora),
                tipo: evento.type
            });
            setCreateModalMode('edit')
            setCreateModalOpen(true);
        }
        // Abrir modal en CREAR si no hay evento
        else {
            setCreateModalData({
                start: toISO8601(hora),
                end: toISO8601(hora + 1),
                topics: [],
                avaliableTopics: professionalTopics,
                day: diaStr,
                week_day: obtenerDiaDeLaSemana(diaStr),
                recurrent: false,
            });
            setCreateModalMode('create')
            setCreateModalOpen(true);
        }
    };

    // --- cierro el modal ------------------------------------------------------------------------
    const handleCloseCreateModal = () => {
        setCreateModalOpen(false);
        setCreateModalData(null);
    };

    // --- guardo nueva tarea ---------------------------------------------------------------------
    const handleSaveNewTask = async (newTask) => {
      try {
        if (newTask.recurrent) {
          if (newTask.week_day == 0) newTask.week_day = 7
          await postRecurrent(prof_id, newTask);
        }
        else {
          await postSpecific(prof_id, newTask);
        }

        setCreateModalOpen(false);
        setCreateModalData(null);
        await cargarEventos(prof_id);
      } catch (error) {
        console.error('Error al guardar la tarea:', error);
      }
    };

    // --- edito una tarea ------------------------------------------------------------------------
    const handleEditTask = async (oldTask, updatedTask) => {
      try {
        let data = {}
        console.log(oldTask)
        switch (oldTask.tipo) {
          case 'recurrent':
            if (updatedTask.week_day == 0) updatedTask.week_day = 7
            if (oldTask.week_day == 0) oldTask.week_day = 7
            data = {
              week_day: oldTask.week_day,
              start: oldTask.start,
              Nweek_day: updatedTask.week_day,
              Nstart: updatedTask.start,
              Nend: updatedTask.end,
              topics: updatedTask.topics
            }
            await putRecurrent(prof_id, data)
            break
          case 'specific':
            data = {
              day: oldTask.day,
              start: oldTask.start,
              Nday: updatedTask.day,
              Nstart: updatedTask.start,
              Nend: updatedTask.end,
              topics: updatedTask.topics
            }
            await putSpecific(prof_id, data)
            break
          case 'exception':
            data = {
              day: oldTask.day,
              start: oldTask.start,
              Nday: updatedTask.day,
              Nstart: updatedTask.start,
              Nend: updatedTask.end
            }
            await putException(prof_id, data)
            break
          default: console.error('Invalid task type')
          }
          await cargarEventos(prof_id);
      } catch (error) {
        console.error('Error al editar la tarea:', error);
      }
    }

    // --- borro una tarea ------------------------------------------------------------------------
    const handleDeleteTask = async (eventToDelete) => {
      try {
        switch (eventToDelete.tipo) {
          case 'recurrent':
            if (eventToDelete.week_day == 0) eventToDelete.week_day = 7
            await deleteRecurrent(prof_id, eventToDelete)
            break
          case 'specific':
            await deleteSpecific(prof_id, eventToDelete)
            break
          case 'exception':
            await deleteException(prof_id, data)
            break
        }
        await cargarEventos(prof_id);
      } catch (error) {
        console.error('Error al borrar la tarea:', error);
      }
    };

    // --- cancelo tarea por unica vez ------------------------------------------------------------
    const handleCancelOneOccurrence = async (eventToCancel) => {
      try {
        await postException(prof_id, eventToCancel);
        await cargarEventos(prof_id);
      } catch (error) {
        console.error('Error al guardar la tarea:', error);
      }
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
          onSaveTask={handleSaveNewTask}
          onEditTask={handleEditTask}
          mode={createModalMode}
          onDeleteTask={handleDeleteTask}
          onCancelOneOccurrence={handleCancelOneOccurrence}
      />

    </div>
  );
};

export default Calendario;
