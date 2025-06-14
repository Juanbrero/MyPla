import React, { useState, useEffect } from 'react';
import CeldaHora from '../studentCalendar/CeldaHoraStudent.jsx';
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, setHours, setMinutes, weeksToDays} from 'date-fns';
import { es } from 'date-fns/locale';
import { getAvailableStudent } from '../../services/available/avaliable-student.service.js';
import ReservationModal from '../reservation/ReservationModal.jsx';
import { useParams } from 'react-router-dom';
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
    if (!eventos) return { available: [], exception: [] };

    const { available = [], exception = [] } = eventos;

    // Filtrar específicos para el día
    const availableDelDia = available.filter(e => isSameDay(parseISO(e.day), dia));

    // Filtrar excepciones para el día
    const excepcionesDelDia = exception.filter(e => isSameDay(parseISO(e.day), dia));

    // // Filtrar recurrentes para el día, omitiendo los que tienen excepción y que coincidan con la hora
    // const recurrentesDelDia = recurrent.filter(e => {
    //     const esElDia = getDay(dia) === e.week_day;
    //     const horaEv = horaNumero(parseHora(e.start));
    //     const tieneExcepcion = excepcionesDelDia.some(exc => {
    //         const horaInicioRecurrente = parseHora(e.start);
    //         const horaInicioExcepcion = parseHora(exc.start);
    //         return esElDia && horaInicioRecurrente === horaInicioExcepcion;
    //     });
    //     return esElDia;
    //     // return esElDia && !tieneExcepcion;
    // });
    return {
        available: availableDelDia,
        exception: excepcionesDelDia,
    };
};

const StudentCalendar = ({token}) => {
    const { prof_id } = useParams() 
    useEffect(() => {
        document.title = "MiPla - Calendario";
    }, []);

    // estados del modal
    const [modalOpen, setModalOpen] = useState(false);
    const [modalData, setModalData] = useState(null); 

    // dia de inicio de la semana 
    const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));

    // datos de la bd
    const [eventos, setEventos] = useState({});

    // --- hago click en una celda ---------------------------------------------------------------
    const handleCeldaClick = (dia, hora, evento = null) => {
        // Abrir modal en EDITAR si hay evento
        const diaStr = format(dia, 'yyyy-MM-dd')
        if (evento) {
          if (evento.type === 'available') {
            console.log(evento)
            setModalData({
              start: `${evento.start}.000Z`,
              end: `${evento.end}.000Z`,
              topics: evento.topics,
              day: evento.day,
              selectedHour: toISO8601(hora),
              tipo: evento.type 
            });
            setModalOpen(true);
          }
        }
    };

    // --- cierro el modal ------------------------------------------------------------------------
    const handleCloseModal = () => {
        setModalOpen(false);
        setModalData(null);
    };

    // --- guardo nueva tarea ---------------------------------------------------------------------
    const handleSaveNewTask = async (newTask) => {
      try {
        if (newTask.recurrent) {
          await postRecurrent(token, newTask);
        }
        else {
          await postSpecific(token, newTask);
        }
        setModalOpen(false);
        setModalData(null);
        await cargarEventos(token);
      } catch (error) {
        console.error('Error al guardar la tarea:', error);
      }
    };

    // --- cargo los EVENTOS de la base de datos --------------------------------------------------
    const cargarEventos = async (_token) => {
        try {
            const data = await getAvailableStudent(_token, prof_id, format(semanaInicio, 'yyyy-MM-dd'));
            setEventos(data);
        } catch (error) {
            console.error("Error cargando eventos:", error);
        }
    };

    useEffect(() => {
        cargarEventos(token);
    }, [prof_id]);

    const siguienteSemana = () => setSemanaInicio(addDays(semanaInicio, 7));
    const anteriorSemana = () => setSemanaInicio(addDays(semanaInicio, -7));

    const diasSemana = Array.from({ length: 7 }).map((_, i) => addDays(semanaInicio, i));

    // obtengo los eventos en cada dia que se muestra en la agenda
    const eventosPorDia = diasSemana.reduce((acc, dia) => {
        acc[format(dia, 'yyyy-MM-dd')] = filtrarEventosPorDia(eventos, dia);
        return acc;
    }, {});

    return (
    <div className="p-4-calendario">
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

      <ReservationModal
          open={modalOpen}
          onClose={handleCloseModal}
          taskData={modalData}
          token={token}
          prof_id={prof_id}
      />

    </div>
  );
};

export default StudentCalendar;
