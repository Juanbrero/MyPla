import React, { useState } from "react";
import ScheduleEdit from '../components/ScheduleEdit';
import ScheduleCreate from '../components/ScheduleCreate';
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { DateTime } from "luxon";


function Calendar() {

  const [isCreated, setCreated] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  // const [selectedTask, setSelectedTask] = useState({
  //    topics: ['Estrategia', 'Marketing'],
  //    day: 'Lunes',
  //    start: '14:00',
  //    end: '15:00',
  //    recurrent: true,
  //    date: "2025-04-18",
  // });
  const [selectedTask, setSelectedTask] = useState({
     topics: [],
     day: '',
     start: '',
     end: '',
     recurrent: true,
     date: "",
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

  const [clickedEvent, setClickedEvent] = useState(null);


  const handleSelect = (info) => {
 
    setCreated(false);
    const start = DateTime.fromISO(info.startStr);
    const end = DateTime.fromISO(info.endStr);
    
    setSelectedTask({
      // topics: ['Estrategia', 'Marketing'],
      topics: [],
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
    
    let evento = {
      title: arg.event.title,
      daysOfWeek: arg.event.extendedProps.daysOfWeek,
      day: arg.event.extendedProps.day,
      date: arg.event.extendedProps.date,
      start: arg.event.start,
      startTime: arg.event.extendedProps.startTime,
      end: arg.event.end,
      endTime: arg.event.extendedProps.endTime,
      recurrent: arg.event.extendedProps.recurrent,
      eventTopics: arg.event.extendedProps.eventTopics,
    };
    
    setClickedEvent(evento);
    console.log("evento clickeado: ", evento);
    setCreated(true);
    setModalOpen(true);
    // alert(`Evento: ${arg.event.title}`);
    // mostrar information
  };

  const handleSaveTask = (taskName) => {
    
    const baseProps = {
      recurrent: taskName.recurrent,
      eventTopics: taskName.topics || [], // por si no está definido
    };

    const newEvent = {
      title: '',
      color: taskName.recurrent ? 'green' : 'orange',
      extendedProps: baseProps,      
    }

    if (taskName.recurrent) {
      const dayIndex = dias.indexOf(taskName.day);
      newEvent.daysOfWeek = [dayIndex];
      newEvent.day = taskName.day;
      newEvent.startTime = taskName.start;
      newEvent.endTime = taskName.end;
      newEvent.extendedProps = {
        ...baseProps,
        daysOfWeek : [dayIndex],
        day : taskName.day,
        startTime : taskName.start,
        endTime : taskName.end,
      };
    } 
    else {
      const eventDate = taskName.date;
      newEvent.start = `${eventDate}T${taskName.start}`;
      newEvent.end = `${eventDate}T${taskName.end}`;
      newEvent.extendedProps = {
        ...baseProps,
        date : eventDate,
      }
    }

    console.log("newEvent: ", newEvent);

    setEvents([...events, 
      newEvent
    ])
    handleCloseModal()
  };

  const handleDeleteTask = (taskName) => {


  }


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
        eventClick={handleEventClick}
        events={events}
        height={"90vh"}
      />
      <>
        {isCreated ? (
          <ScheduleEdit
            open={modalOpen}
            clickedEvent={clickedEvent}
            onClose={handleCloseModal}
            taskData={selectedTask}
            // onCancelSlot={handleCancelSlot}
            onCancelTask={handleCancelTask}
            onSaveTask={handleSaveTask}
          />
        ) : (
          <ScheduleCreate
            open={modalOpen}
            onClose={handleCloseModal}
            taskData={selectedTask}
            // onCancelSlot={handleCancelSlot}
            onCancelTask={handleCancelTask}
            onSaveTask={handleSaveTask}
          />
        )}
      </>
    </div>
  );
}

export default Calendar;
