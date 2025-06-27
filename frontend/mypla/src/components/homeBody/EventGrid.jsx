import { EventCard } from './EventCard';


export const EventGrid = ({ events, onSelectEvent }) => {
  
  if (!Array.isArray(events)) return null;

  return (
    <section className="event-section">
      <h2>Próximos Eventos</h2>
      <div className="event-grid">
        {events.map(event => (
          <EventCard key={events.indexOf(event)} event={event} onClick={onSelectEvent}/>
        ))}
      </div>
    </section>
  );
};
