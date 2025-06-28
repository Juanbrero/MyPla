import './EventCard.css';
import dayjs from "dayjs";


export const EventCard = ({ event , onClick}) => {

  const { creator, day_hour, duration, invites, price, topic, title } = event;

  const [date, hour] = day_hour.split("T");
  const [hours, minutes] = hour.split(":");

  const formattedHour = `${hours}:${minutes}`;
 
  const dateObj = dayjs(day_hour).toDate();

  const day = dateObj.toLocaleDateString('es-AR', { day: '2-digit' });
  const month = dateObj.toLocaleDateString('es-AR', { month: 'short' }).toUpperCase();
  const weekday = dateObj.toLocaleDateString('es-AR', { weekday: 'short' }).toUpperCase();

  const select = () => {
    console.log("evento seleccionado: ", event);
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
        {invites.length > 0 && (
          <p><strong>Invitados:</strong> {invites.join(', ')}</p>
        )}
        <p><strong>Hora de inicio:</strong> {formattedHour}hs</p>
        <p><strong>Duracion:</strong> {(duration / 60)}hs</p>
        <p><strong>Valor de inscripcion:</strong> ${price}</p>
        <span className="event-category">{topic}</span>
      </div>
    </div>
  );
};



