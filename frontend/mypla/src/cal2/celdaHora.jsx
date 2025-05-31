import React from 'react';
import { setHours, setMinutes, parseISO, isSameDay } from 'date-fns';

const parseHora = (horaStr) => {
  if (!horaStr) return '';
  return horaStr.slice(0, 5);
};

const eventoEnHora = (eventos, dia, hora) => {
  for (const ev of eventos) {
    let inicio;
    if (ev.day) {
      inicio = parseISO(ev.day + 'T' + ev.start);
    } else if (ev.start) {
      const horaStr = ev.start.slice(0, 5);
      const h = parseInt(horaStr.slice(0, 2));
      const m = parseInt(horaStr.slice(3, 5));
      inicio = setMinutes(setHours(dia, h), m);
    }

    if (inicio && isSameDay(inicio, dia) && inicio.getHours() === hora) {
      return ev;
    }
  }
  return null;
};

const CeldaHora = ({ dia, hora, eventosDelDia, onClick }) => {
  const { recurrent = [], specific = [] } = eventosDelDia || {};
  const todosEventos = [...recurrent, ...specific];

  // const { recurrent = [], specific = [], exceptions = [] } = eventosDelDia || {};
  // const todosEventos = [...recurrent, ...specific, exceptions];

  const evento = eventoEnHora(todosEventos, dia, hora);
  
  let claseCelda = 'celda-hora'
  
  if (evento) {
    claseCelda += ' celda-hora-ocupada'
    if (evento.type == 'recurrent') {
      claseCelda += ' celda-recurrent'
    }
    else if (evento.type == 'specific') {
      claseCelda += ' celda-specific'
    }
    else if (evento.type == 'exception') {
      claseCelda += ' celda-exception'
    }
  }
  // const claseCelda = evento ? 'celda-hora-ocupada' : 'celda-hora';
  
  return (
    <div className={claseCelda} onClick={() => onClick(dia, hora, evento)}>
      {evento ? (
        <span title={evento.topics ? evento.topics.join(', ') : 'Evento'}>
          {evento.start ? parseHora(evento.start) : ''}
          {evento.topics ? ` - ${evento.topics.join(', ')}` : ''}
        </span>
      ) : (
        '\u00A0'
      )}
    </div>
  );
};

export default CeldaHora;
