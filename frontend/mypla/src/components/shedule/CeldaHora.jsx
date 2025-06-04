import React from 'react';
import { setHours, setMinutes, parseISO, isSameDay } from 'date-fns';

const parseHora = (horaStr) => {
  if (!horaStr) return '';
  return horaStr.slice(0, 5);
};

const eventoEnHora = (eventos, dia, hora) => {
  for (const ev of eventos) {
    let inicio, fin;

    if (ev.day) {
      inicio = parseISO(ev.day + 'T' + ev.start);
      fin = parseISO(ev.day + 'T' + ev.end);
    } else if (ev.start && ev.end) {
      const horaInicioStr = ev.start.slice(0, 5);
      const horaFinStr = ev.end.slice(0, 5);
      const hInicio = parseInt(horaInicioStr.slice(0, 2));
      const mInicio = parseInt(horaInicioStr.slice(3, 5));
      const hFin = parseInt(horaFinStr.slice(0, 2));
      const mFin = parseInt(horaFinStr.slice(3, 5));
      inicio = setMinutes(setHours(dia, hInicio), mInicio);
      fin = setMinutes(setHours(dia, hFin), mFin);
    }

    if (inicio && fin && isSameDay(inicio, dia)) {
      const inicioHora = inicio.getHours();
      const finHora = fin.getHours();

      if (hora >= inicioHora && hora < finHora) {
        let posicion = 'middle';
        if (hora === inicioHora) {
          posicion = hora === finHora - 1 ? 'only' : 'start';
        }
        else if (hora === finHora - 1) posicion = 'end';

        return { evento: ev, posicion };
      }
    }
  }
  return { evento: null, posicion: null };
};


const CeldaHora = ({ dia, hora, eventosDelDia, onClick }) => {
  const { recurrent = [], specific = [], exception = [] } = eventosDelDia || {};
  const todosEventos = [...exception, ...recurrent, ...specific];

  const { evento, posicion } = eventoEnHora(todosEventos, dia, hora);

  let claseCelda = 'celda-hora';
if (evento) console.log(evento)
  if (evento) {
    claseCelda += ' celda-hora-ocupada';
    if (evento.type == 'recurrent') {
      claseCelda += ' celda-recurrent';
    } else if (evento.type == 'specific') {
      claseCelda += ' celda-specific';
    } else if (evento.type == 'exception') {
      claseCelda += ' celda-exception';
    }

    if (posicion === 'start') {
      claseCelda += ' celda-inicio';
    } else if (posicion === 'end') {
      claseCelda += ' celda-fin';
    } else if (posicion === 'only') {
      claseCelda += ' celda-unica';
    }
  }

  return (
    <div className={claseCelda} onClick={() => onClick(dia, hora, evento)}>
      {evento && posicion === 'start' || evento && posicion === 'only'  ? (
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
