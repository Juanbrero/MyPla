import './EventCard.css';
import dayjs from "dayjs";


export const EventCard = ({ event , onClick}) => {
  const { title, date, hora, precio, creator, participants, topic } = event;


  const dateObj = dayjs(date).toDate();

  const day = dateObj.toLocaleDateString('es-AR', { day: '2-digit' });
  const month = dateObj.toLocaleDateString('es-AR', { month: 'short' }).toUpperCase();
  const weekday = dateObj.toLocaleDateString('es-AR', { weekday: 'short' }).toUpperCase();

  const select = () => {
    onClick?.(event);
  }


  return (
    <div className={`event-card category-${topic.toLowerCase()}`} onClick={select}>
      <div className="event-card-date">
        <span className="weekday">{weekday}</span>
        <span className="day">{day}</span>
        <span className="month">{month}</span>
      </div>
      <div className="event-card-body">
        <h3>{title}</h3>
        <p><strong>Host:</strong> {creator}</p>
        {participants.length > 0 && (
          <p><strong>Invitados:</strong> {participants.join(', ')}</p>
        )}
        <p><strong>Hora de inicio:</strong> {hora}hs</p>
        <p><strong>Valor de inscripcion:</strong> ${precio}</p>
        <span className="event-category">{topic}</span>
      </div>
    </div>
  );
};



