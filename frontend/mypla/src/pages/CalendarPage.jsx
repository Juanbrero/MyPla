import React, { useState } from "react";
import ScheduleInformation from '../components/ScheduleInformation';
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { DateTime } from "luxon";

function Calendar() {

  console.log("Renderizando CalendarPage");


  const [modalOpen, setModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState({
     topics: ['Estrategia', 'Marketing'],
     day: 'Lunes',
     start: '14:00',
     end: '15:00',
     recurrent: true,
     date: "2025-04-18",
  });

  const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

  const [events, setEvents] = useState([
    {
      title: "Evento de prueba",
      start: '2025-04-22T14:00:00',
      end: '2025-04-22T15:30:00',
      color: 'red'
    },
  ])
  const handleSelect = (info) => {
    console.log(info)
    const start = DateTime.fromISO(info.startStr)
    const end = DateTime.fromISO(info.endStr)
    setSelectedTask({
      topics: ['Estrategia', 'Marketing'],
      day: dias[new Date(start).getDay()],
      start: start.toFormat("HH:mm"),
      end: end.toFormat("HH:mm"),
      recurrent: false,
      date: start.toFormat("yyyy-MM-dd"),
    })
    setModalOpen(true);
    // mostrar create
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleCancelTask = (taskName) => {
    setModalOpen(false);
  };

  const handleEventClick = (arg) => {
    alert(`Evento: ${arg.event.title}`);
    // mostrar information
  };

  const handleSaveTask = (taskName) => {
    const newEvent = {
      title: 'evento',
      color: 'green',
    }
    if (taskName.day) {
      newEvent.daysOfWeek = [dias.indexOf(taskName.day)]
      newEvent.startTime = taskName.start + ':00'
      newEvent.endTime = taskName.end + ':00'
    } else {
      const dateO = DateTime.fromISO(taskName.date)
      console.log(dateO.day)
      const [startHour, startMinute] = taskName.start.split(":").map(Number);
      const [endHour, endMinute] = taskName.end.split(":").map(Number);
      newEvent.start = dateO.set({hour: startHour, minute: startMinute}).toISO()
      newEvent.end = dateO.set({hour: endHour, minute: endMinute}).toISO()
    }
    setEvents([...events, 
      newEvent
    ])
    handleCloseModal()
  };

  console.log("selected task: " + selectedTask.topics);

  return (
    <div>
      <p>Calendario debería aparecer aquí</p>

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
        eventClick={handleEventClick}
        events={events}
        height={"90vh"}
      />
      {/* agregar condicion para ver si abro create o info. */}
      <ScheduleInformation
        open={modalOpen}
        onClose={handleCloseModal}
        taskData={selectedTask}
        // onCancelSlot={handleCancelSlot}
        onCancelTask={handleCancelTask}
        onSaveTask={handleSaveTask}
      />
    </div>
  );
}

export default Calendar;
