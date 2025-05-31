import React from 'react';
import { format, setHours, setMinutes, parseISO, isSameDay } from 'date-fns';

const obtenerFechaConHora = (dia, hora) => {
  return setMinutes(setHours(dia, hora), 0);
};

const eventoEnHora = (eventos, dia, hora) => {
  // Buscar evento que inicie en esa fecha+hora
  for (const ev of eventos) {
    let inicio;
    if (ev.day) {
      // específico o excepción
      inicio = parseISO(ev.day + 'T' + ev.start); 
      // (Si el backend manda separado day y start)
    } else if (ev.start) {
      // recurrente: la fecha no viene, pero comparo hora
      // Lo que hiciste antes: evento recurrente ya filtrado para el día
      inicio = setMinutes(setHours(dia, parseInt(ev.start.slice(0, 2))), parseInt(ev.start.slice(3, 5)));
    }

    if (inicio && isSameDay(inicio, dia) && inicio.getHours() === hora) {
      return ev;
    }
  }
  return null;
};

const CeldaHora = ({ dia, hora, eventosDelDia, onClick }) => {
  const { recurrent = [], specific = [], exception = [] } = eventosDelDia || {};

  // Combinar recurrent y specific, no mostramos excepciones
  const todosEventos = [...recurrent, ...specific];
  const evento = eventoEnHora(todosEventos, dia, hora);

  // Decidir clase para la celda según si tiene evento
  const claseCelda = evento ? 'celda-hora-ocupada' : 'celda-hora';

  return (
    <div className={claseCelda} onClick={() => onClick(dia, hora, evento)}>
      {evento ? (
        <span title={evento.description || 'Evento'}>
          {evento.start ? evento.start.slice(0, 5) : ''} {/* mostrar hh:mm */}
          {evento.description ? ` - ${evento.description}` : ''}
        </span>
      ) : (
        '\u00A0' // espacio no rompible para mantener tamaño
      )}
    </div>
  );
};

export default CeldaHora;
