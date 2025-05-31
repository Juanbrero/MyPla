import React, { useState, useEffect } from 'react';
import CeldaHora from './celdaHora.jsx';
import { prof_id } from "../utils/testData";
import { getAvailableProfessional } from './service.js';
import { startOfWeek, addDays, format, isSameDay, getDay, parseISO, setHours, setMinutes } from 'date-fns';
import './calendario.css';

// --- funciones utilitarias para hora ---
const parseHora = (horaStr) => {
  if (!horaStr) return '';
  return horaStr.slice(0, 5);
};

const horaNumero = (horaStr) => {
  if (!horaStr) return null;
  return parseInt(horaStr.slice(0, 2), 10);
};

// --- filtrar eventos por día adaptado ---
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

const horasDelDia = Array.from({ length: 13 }, (_, i) => i + 8); // 8 a 20

const Calendario = () => {
  const [semanaInicio, setSemanaInicio] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));
  const [eventos, setEventos] = useState({});
  const [modalInfo, setModalInfo] = useState(null);

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

  const handleCeldaClick = (dia, hora, evento = null) => {
    const fechaHora = setMinutes(setHours(dia, hora), 0);
    setModalInfo({ fechaHora, evento });
    console.log("Abrir modal con:", { fechaHora, evento });
  };

  const eventosPorDia = diasSemana.reduce((acc, dia) => {
    acc[format(dia, 'yyyy-MM-dd')] = filtrarEventosPorDia(eventos, dia);
    return acc;
  }, {});

  return (
    <div className="p-4">
      <div className="calendario-controles">
        <button onClick={anteriorSemana}>⬅️ Anterior</button>
        <h2 className="text-xl font-bold">{format(semanaInicio, "'Semana de' dd/MM/yyyy")}</h2>
        <button onClick={siguienteSemana}>Siguiente ➡️</button>
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
