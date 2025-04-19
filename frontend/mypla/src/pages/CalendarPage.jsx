import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

function Calendar() {
  const handleDateClick = (arg) => {
    alert(`Click en celda vacía: ${arg.dateStr}`);
  };

  const handleEventClick = (arg) => {
    alert(`Evento: ${arg.event.title}`);
  };

  const handleSelect = (info) => {
    const title = prompt("Título del nuevo evento:");
    if (title) {
      alert(`Nuevo evento: "${title}" de ${info.startStr} a ${info.endStr}`);
      // acá podrías hacer setEvents([...events, { title, start: info.startStr, end: info.endStr }])
    }
  };

  return (
    <div>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        headerToolbar={{
          start: "today prev,next",
          center: "title",
          end: "dayGridMonth,timeGridWeek,timeGridDay",
        }}
        selectable={true}
        select={handleSelect}
        dateClick={handleDateClick}
        eventClick={handleEventClick}
        events={[
          {
            title: "Evento de prueba",
            start: new Date().toISOString().slice(0, 10),
          },
        ]}
        height={"90vh"}
      />
    </div>
  );
}

export default Calendar;
