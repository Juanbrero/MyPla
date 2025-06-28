import React, { useState, useEffect } from 'react';
import CeldaHoraMyStudent from './CeldaHoraMyStudent.jsx';
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, isToday} from 'date-fns';
import { es } from 'date-fns/locale';
import StudentReservationModal from './StudentReservationModal.jsx';
import { useParams } from 'react-router-dom';
import { getStudentReservations, cancelStudentReservations } from '../../services/reservation/initial-class.service.js';
import { getCalificate } from '../../services/calification/calification.service.js';
import CalificationsPendingAlert from '../califications/CalificationsPendingAlert.jsx';

// --- CONST: horas del calendario ----------------------------------------------------------
const horasDelDia = Array.from({ length: 24 }, (_, i) => i + 0); // 0 a 23

// --- funciones utilitarias para fechas y horas --------------------------------------------
function sumarUnaHora(horaStr) {
  let [hh, mm, ss] = horaStr.split(":").map(Number);
  hh = (hh + 1) % 24; // Sumar 1 y controlar que no pase de 23
  return `${hh.toString().padStart(2, "0")}:${mm.toString().padStart(2, "0")}:${ss.toString().padStart(2, "0")}`;
}

const toISO8601 = (hora, minutos = '00') => {
  return `${String(hora).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:00.000Z`;
};

// --- obtener los eventos de cada dia ------------------------------------------------------
const filtrarEventosPorDia = (eventos, dia) => {
    if (Object.keys(eventos).length === 0) return { reservations: [] };
    
    // Filtrar específicos para el día
    const reservationsDelDia = eventos.filter(e => isSameDay(parseISO(e.day), dia));
    return {
        reservations: reservationsDelDia,
    };
};


const StudentMyCalendar = ({token}) => {
    useEffect(() => {
        document.title = "MiPla - Calendario";
    }, []);
    
    const [openAlert, setOpenAlert] = useState(false);

    useEffect(() => {
      const verificarCalificacionesPendientes = async () => {
        try {
          const response = await getCalificate(token);
          const califPendings = response.data;

          // Mostrar la alerta si hay al menos una calificación pendiente
          if (Array.isArray(califPendings) && califPendings.length > 0) {
            setOpenAlert(true);
          }
        } catch (error) {
          console.error("Error al verificar calificaciones pendientes:", error);
        }
      };

      verificarCalificacionesPendientes();
    }, [token]);


  
    // estados del modal
    const [modalOpen, setModalOpen] = useState(false);
    const [modalData, setModalData] = useState(null); 

    // dia de inicio de la semana 
    const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));

    // datos de la bd
    const [eventos, setEventos] = useState({});

    // --- hago click en una celda ---------------------------------------------------------------
    const handleCeldaClick = (dia, hora, evento = null) => {
        if (evento) {
          setModalData(evento)
          evento.topics = []
          evento.topics.push(evento.topic)
          setModalOpen(true);
        }
    };

    // --- cierro el modal ------------------------------------------------------------------------
    const handleCloseModal = () => {
        setModalOpen(false);
        setModalData(null);
    };

    const handleCancelarReserva = async (data) => {
        const res = await cancelStudentReservations(token, `${data.day}T${data.start}`, data.prof_id)
        if (res.error) alert('No se pueden cancelar reservas cercanas o previas a la fecha') 
        await cargarEventos(token);
    }

    // --- cargo los EVENTOS de la base de datos --------------------------------------------------
    const cargarEventos = async (_token) => {
        try {
            const data = await getStudentReservations(token)
            const ev = data['data']['reservations']
            const eventos2 = []
            ev.forEach(element => {
              const [f, h] = element.day_hour.split("T");
              const elem2 = {
                day: f,
                start: h,
                end: sumarUnaHora(h),
                topic: element.topic,
                prof_id: element.prof_id,
                prof_username: element.prof_username,
                link_class: element.link_class,
              }
              eventos2.push(elem2)
            });
            setEventos(eventos2);
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
                <CeldaHoraMyStudent
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

      <StudentReservationModal
          open={modalOpen}
          onClose={handleCloseModal}
          taskData={modalData}
          onDeleteTask={handleCancelarReserva}
      />

      {openAlert && (
        <CalificationsPendingAlert open={openAlert} onClose={() => setOpenAlert(false)} />
      )}



    </div>
  );
};

export default StudentMyCalendar;
