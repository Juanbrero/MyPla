import { EventCard } from './EventCard';


export const EventGrid = ({ events }) => {
  if (!Array.isArray(events)) return null;

  return (
    <section className="event-section">
      <h2>Próximos Eventos</h2>
      <div className="event-grid">
        {events.map(event => (
          <EventCard key={event.id} event={event} />
        ))}
      </div>
    </section>
  );
};
