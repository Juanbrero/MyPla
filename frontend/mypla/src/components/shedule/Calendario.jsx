import React, { useState, useEffect } from 'react';
import CeldaHora from './CeldaHora.jsx';
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, isToday} from 'date-fns';
import { es, fi } from 'date-fns/locale';
import './calendario.css';
import ScheduleModal from './ScheduleModal.jsx';
import { getAvailableProfessional } from '../../services/available/available-professional.service.js';
import { postSpecific, putSpecific, deleteSpecific } from '../../services/specific/specific.service';
import { postRecurrent, putRecurrent, deleteRecurrent } from '../../services/recurrent/recurrent.service';
import { postException, putException, deleteException } from '../../services/exception/exception.service';
import { postEvents } from '../../services/events/events.service.js';
import { getProfessionalTopics } from '../../services/professionals-topic/professionals-topic.service.js';
import { ColorReferenceHelp } from './schedule-components/ColorReferenceHelp.jsx';
import { cancelStudentReservations } from '../../services/reservation/initial-class.service.js';
import { getAllProfessionals } from '../../services/professionals/professionals.service.js';
import ProfessionalReservationModal from './ProfessionalRecervationModal.jsx';
import SelectTipoDisponibilidadModal from './SelectTipoDisponibilidadModal.jsx';
import CrearEventoModal from './CrearEventoModal.jsx';
import InvitesPendingAlert from '../invites/InvitesPendingAlert.jsx'
import { getInvites } from '../../services/invites/invites.service.js';
import VerEventoModal from './VerEventoModal.jsx';


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
     if (!eventos) return { recurrent: [], specific: [], exception: [], class_: [], guest: [], my_events: [] };

     const { class_ = [], recurrent = [], specific = [], exception = [], guest = [], my_events = [] } = eventos;

    // Filtrar específicos para el día
    const especificosDelDia = specific.filter(e => isSameDay(parseISO(e.day), dia));

    // Filtrar excepciones para el día
    const excepcionesDelDia = exception.filter(e => isSameDay(parseISO(e.day), dia));
    // Filtrar excepciones para el día
    const clasesDelDia = class_.filter(e => isSameDay(parseISO(e.day), dia));

    const guestDelDia = guest.filter(e => isSameDay(parseISO(e.day_hour.slice(0, 10)), dia));
    const myevDelDia = my_events.filter(e => isSameDay(parseISO(e.day_hour.slice(0, 10)), dia));

    // Filtrar recurrentes para el día, omitiendo los que tienen excepción y que coincidan con la hora
    const recurrentesDelDia = recurrent.filter(e => {
        const esElDia = getDay(dia) === e.week_day;
        const horaEv = horaNumero(parseHora(e.start));
        const tieneExcepcion = excepcionesDelDia.some(exc => {
            const horaInicioRecurrente = parseHora(e.start);
            const horaInicioExcepcion = parseHora(exc.start);
            return esElDia && horaInicioRecurrente === horaInicioExcepcion;
        });
        return esElDia;
        // return esElDia && !tieneExcepcion;
    });

    return {
        recurrent: recurrentesDelDia,
        specific: especificosDelDia,
        exception: excepcionesDelDia,
        clases: clasesDelDia,
        guest: guestDelDia,
        my_events: myevDelDia
    };
};

const Calendario = ({token}) => {
    useEffect(() => {
      document.title = "Mipla - Calendario";
    }, []);

    // alerta de invitaciones pendientes
    const [openAlert, setOpenAlert] = useState(false);
    
    useEffect(() => {
      const verificarInvitacionesPendientes = async () => {
        try {
          const response = await getInvites(token);
          const invitePendings = response.data;
          
          // Mostrar la alerta si hay al menos una invitacion pendiente
          if (Array.isArray(invitePendings) && invitePendings.length > 0) {
            setOpenAlert(true);
            console.log("entra");
          }
        } catch (error) {
          console.error("Error al verificar invitaciones pendientes:", error);
        }
      };

      verificarInvitacionesPendientes();
    }, [token]);



    // estados del modal
    const [modalOpen, setModalOpen] = useState(false);
    const [modalData, setModalData] = useState(null); 
    const [modalMode, setModalMode] = useState('create') // 'create', 'edit', 'exception'

    // modal reserva
    const [modalBOpen, setModalBOpen] = useState(false);
    const [modalBData, setModalBData] = useState(null); 

    // modal seleccionar
    const [modalSOpen, setModalSOpen] = useState(false);

    // modal evento
    const [modalEOpen, setModalEOpen] = useState(false);
    const [modalEData, setModalEData] = useState(null); 

    // modal ver evento
    const [modalVOpen, setModalVOpen] = useState(false);
    const [modalVData, setModalVData] = useState(null); 

    // dia de inicio de la semana 
    const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));

    // datos de la bd
    const [eventos, setEventos] = useState({});
    const [professionalTopics, setProfessionalTopics] = useState([]);
    const [professors, setProfessors] = useState([]);

    // --- hago click en una celda ---------------------------------------------------------------
    const handleCeldaClick = (dia, hora, evento = null) => {
      if (professionalTopics.length === 0) {
        alert('Aun no seleccionaste tus tópicos')
        return
      }
        // Abrir modal en EDITAR si hay evento
        const diaStr = format(dia, 'yyyy-MM-dd')
        if (evento) {
          if (evento.type === 'class_') {
            setModalBData(evento)
            setModalBOpen(true)
          }
          else if (evento.type === 'recurrent' || evento.type === 'specific') {
            setModalData({
              start: `${evento.start}.000Z`,
              end: `${evento.end}.000Z`,
              topics: evento.topics,
              avaliableTopics: professionalTopics,
              day: evento.day ? evento.day : diaStr, //si es recurrente envio el dia en que se clickea para la generacion de excepciones
              week_day: evento.week_day,
              recurrent: evento.type === 'recurrent',
              selectedHour: toISO8601(hora),
              tipo: evento.type
            });
            setModalMode('edit')
            setModalOpen(true);
          }
          else if (evento.type === 'exception') {
            setModalData({
              start: `${evento.start}.000Z`,
              end: `${evento.end}.000Z`,
              day: evento.day,
            })
            setModalMode('exception')
            setModalOpen(true);
          }
          else if (evento.type === 'my_events') {
            console.log(evento)
            setModalVData({
              start: `${evento.day_hour.slice(-8)}.000Z`,
              end: `${evento.end.slice(-8)}.000Z`,
              day: `${evento.day_hour.slice(0, 10)}`,
              title: evento.title,
              topic: evento.topic,
              price: evento.price,
              guest: evento.guest
            })
            setModalVOpen(true)
          }
          else if (evento.type === 'guest') {
            setModalVData({
              start: `${evento.day_hour.slice(-8)}.000Z`,
              end: `${evento.end.slice(-8)}.000Z`,
              day: `${evento.day_hour.slice(0, 10)}`,
              title: evento.title,
              topic: evento.topic,
              price: evento.price,
              guest: evento.guest
            })
            setModalVOpen(true)
          }
        }
        // Abrir modal en CREAR si no hay evento
        else if (diaStr >= new Date().toISOString().slice(0, 10)){
          setModalData({
            start: toISO8601(hora),
            end: toISO8601(hora + 1),
            topics: [],
            avaliableTopics: professionalTopics,
            day: diaStr,
            week_day: obtenerDiaDeLaSemana(diaStr),
            recurrent: false,
          });
          setModalEData({
            start: toISO8601(hora),
            end: toISO8601(hora + 1),
            topics: [],
            avaliableTopics: professionalTopics,
            day: diaStr,
            selectedTopic: null,
            professors: professors,
          });
          setModalMode('create')
          // setModalOpen(true);
          setModalSOpen(true)
        }
    };

    // --- cierro el modal ------------------------------------------------------------------------
    const handleCloseModal = () => {
        setModalOpen(false);
        setModalData(null);
    };

    const handleCloseModalB = () => {
      setModalBOpen(false);
      setModalBData(null);
    }

    const handleCloseModalS = () => {
      setModalSOpen(false);
      setModalSData(null);
    }

    const handleCloseModalE = () => {
      setModalEOpen(false);
      setModalEData(null);
    }

    const handleCloseModalV = () => {
      setModalVOpen(false);
      setModalVData(null);
    }

    const handleCancelarReserva = async (data) => {
      const res = await cancelStudentReservations(token, `${data.day}T${data.start}`, data.student_id)
      if (res.error) alert('No se pueden cancelar reservas cercanas o previas a la fecha') 
      await cargarEventos(token);
    }

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

    // --- edito una tarea ------------------------------------------------------------------------
    const handleEditTask = async (oldTask, updatedTask) => {
      try {
        let data = {}
        switch (oldTask.tipo) {
          case 'recurrent':
            data = {
              week_day: oldTask.week_day,
              start: oldTask.start,
              Nweek_day: updatedTask.week_day,
              Nstart: updatedTask.start,
              Nend: updatedTask.end,
              topics: updatedTask.topics
            }
            await putRecurrent(token, data)
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
            await putSpecific(token, data)
            break
          case 'exception':
            data = {
              day: oldTask.day,
              start: oldTask.start,
              Nday: updatedTask.day,
              Nstart: updatedTask.start,
              Nend: updatedTask.end
            }
            await putException(token, data)
            break
          default: console.error('Invalid task type')
          }
          await cargarEventos(token);
      } catch (error) {
        console.error('Error al editar la tarea:', error);
      }
    }

    // --- borro una tarea ------------------------------------------------------------------------
    const handleDeleteTask = async (eventToDelete) => {
      try {
        switch (eventToDelete.tipo) {
          case 'recurrent':
            await deleteRecurrent(token, eventToDelete)
            break
          case 'specific':
            await deleteSpecific(token, eventToDelete)
            break
          case 'exception':
            await deleteException(token, data)
            break
        }
        await cargarEventos(token);
      } catch (error) {
        console.error('Error al borrar la tarea:', error);
      }
    };

    // --- cancelo tarea por unica vez ------------------------------------------------------------
    const handleCreateException = async (eventToCancel) => {
      try {
        await postException(token, eventToCancel);
        await cargarEventos(token);
      } catch (error) {
        console.error('Error al guardar la excepcion:', error);
      }
    };

    const handleDeleteException = async (exceptionToCancel) => {
      try {
        await deleteException(token, exceptionToCancel);
        await cargarEventos(token);
        } catch (error) {
          console.error('Error al borrar la excepcion:', error);
      }
    }
    
    // --- abro modal segun corresponda -----------------------------------------------------------

    const handleAbrirDisponibilidad = () => {
      setModalOpen(true)
      setModalSOpen(false)
    }

    const handleAbrirEvento = () => {
      console.log(modalEData)
      setModalEOpen(true)
      setModalSOpen(false)
    }

    const handleSaveEvento = async (newEvent) => {
      const data = {
        day_hour: `${newEvent.day}T${newEvent.start.slice(0, -1)}`,
        duration: (horaNumero(newEvent.end) - horaNumero(newEvent.start)) * 60,
        price: newEvent.precio,
        invites: newEvent.idsProfesionales,
        topic: newEvent.selectedTopic,
        title: newEvent.nombre,
      } 
      console.log(data)
      try {
        await postEvents(token, data);

        setModalEOpen(false);
        setModalEData(null);
        await cargarEventos(token);
      } catch (error) {
        console.error('Error al crear el evento:', error);
      }
    }

    const handleDeleteEvento = async (evento) => {
      // TODO
    }

    // --- cargo los EVENTOS de la base de datos --------------------------------------------------
    const cargarEventos = async (_token) => {
      try {
        const [
          _data,
          _topics,
          _profesionalesDisponibles
        ] = await Promise.all([
          getAvailableProfessional(_token),
          getProfessionalTopics(_token),
          getAllProfessionals()
        ]);

        setEventos(_data);
        setProfessionalTopics(_topics);
        setProfessors(_profesionalesDisponibles.data.professionals);
      } catch (error) {
        console.error("Error cargando eventos:", error);
      }
    };

    useEffect(() => {
        cargarEventos(token);
    }, []);

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
              <div key={`header-${idxDia}`} className={`header-dia ${isToday(dia) ? 'dia-hoy' : ''}`}>
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

      <ScheduleModal
          open={modalOpen}
          onClose={handleCloseModal}
          taskData={modalData}
          onSaveTask={handleSaveNewTask}
          onEditTask={handleEditTask}
          mode={modalMode}
          onDeleteTask={handleDeleteTask}
          onCreateException={handleCreateException}
          onDeleteException={handleDeleteException}
      />

      <ProfessionalReservationModal
          open={modalBOpen}
          onClose={handleCloseModalB}
          taskData={modalBData}
          onDeleteTask={handleCancelarReserva}
      />

      <CrearEventoModal
        open={modalEOpen}
        onClose={handleCloseModalE}
        taskData={modalEData}
        onSaveEvento={handleSaveEvento}
      />

      <VerEventoModal
          open={modalVOpen}
          onClose={handleCloseModalV}
          taskData={modalVData}
          onDeleteEvento={handleDeleteEvento}
      />

      <SelectTipoDisponibilidadModal
          open={modalSOpen}
          onClose={handleCloseModalS}
          onDisponibilidad={handleAbrirDisponibilidad}
          onEvento={handleAbrirEvento}
      />

        <ColorReferenceHelp/>
      {openAlert && (
        <InvitesPendingAlert open={openAlert} onClose={() => setOpenAlert(false)} />
      )}

      <ColorReferenceHelp/>

      </div> 
  );
};

export default Calendario;
