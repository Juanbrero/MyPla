import React, { useState, useEffect } from 'react';
import CeldaHora from './celdaHora.jsx';
import { prof_id } from "../utils/testData";
import { getAvailableProfessional } from './service.js';
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, setHours, setMinutes } from 'date-fns';
import './calendario.css'

const filtrarEventosPorDia = (eventos, dia) => {
  if (!eventos) return { recurrent: [], specific: [], exception: [] };

  const { recurrent = [], specific = [], exception = [] } = eventos;

  // Filtrar especificos para el dia
  const especificosDelDia = specific.filter(e => isSameDay(parseISO(e.day), dia));

  // Filtrar excepciones para el dia
  const excepcionesDelDia = exception.filter(e => isSameDay(parseISO(e.day), dia));

  // Filtrar recurrentes para el dia, omitiendo los que tienen excepción
  const recurrentesDelDia = recurrent.filter(e => {
    const esElDia = getDay(dia) === e.week_day;
    const tieneExcepcion = excepcionesDelDia.some(exc => {
      const horaInicioRecurrente = e.start.slice(0, 8); // 'HH:mm:ss'
      const horaInicioExcepcion = exc.start.slice(0, 8);
      return esElDia && horaInicioRecurrente === horaInicioExcepcion;
    });
    return esElDia && !tieneExcepcion;
  });
  console.log(dia)
if (recurrentesDelDia.length > 0) console.log('rec: ', recurrentesDelDia)
if (especificosDelDia.length > 0) console.log('esp: ', especificosDelDia)
if (excepcionesDelDia.length > 0) console.log('exp', excepcionesDelDia)

  return {
    recurrent: recurrentesDelDia,
    specific: especificosDelDia,
    exception: excepcionesDelDia,
  };
};

const horasDelDia = Array.from({ length: 13 }, (_, i) => i + 8); // Horas de 8 a 20 hs

const Calendario = () => {
  const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 })); // lunes
  const [eventos, setEventos] = useState({}); 
  const [modalInfo, setModalInfo] = useState(null); // Para abrir modal con info del evento o nueva cita

  const cargarEventos = async (profId) => {
    try {
      const data = await getAvailableProfessional(profId);
      setEventos(data);
      console.log("Eventos cargados:", data);
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

  // Abre el modal con info para crear o editar evento
  const handleCeldaClick = (dia, hora, evento = null) => {
    // Creamos Date con la fecha y hora para el modal
    const fechaHora = setMinutes(setHours(dia, hora), 0);
    setModalInfo({ fechaHora, evento });
    console.log("Abrir modal con:", { fechaHora, evento });
    // Aqui llamaria al modal para editar o crear nuevo evento
  };

  // Precalcular eventos filtrados para cada día (solo una vez)
  const eventosPorDia = diasSemana.reduce((acc, dia) => {
    acc[format(dia, 'yyyy-MM-dd')] = filtrarEventosPorDia(eventos, dia);
    return acc;
  }, {});

  return (
    <div className="p-4">
        {/* controles */}
        <div className="calendario-controles">
            <button onClick={anteriorSemana}>⬅️ Anterior</button>
            <h2 className="text-xl font-bold">{format(semanaInicio, "'Semana de' dd/MM/yyyy")}</h2>
            <button onClick={siguienteSemana}>Siguiente ➡️</button>
        </div>

        {/* contenedor */}
        <div className="calendario-contenedor">
            {/* horas */}
            <div className="columna-horas">
                <div className="header-horas"></div> {/* espacio para alinear con header dias */}
                {horasDelDia.map(hora => (
                    <div key={hora} className="hora">{hora}:00</div>
                ))}
            </div>

            {/* dias */}
            <div className="grid-dias">
                {diasSemana.map((dia, idxDia) => (
                    <div key={`header-${idxDia}`} className="header-dia">
                    {format(dia, 'EEE dd/MM')}
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
    </div>

  );
};

export default Calendario;
