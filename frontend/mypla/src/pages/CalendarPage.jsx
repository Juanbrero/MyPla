import React, { useState, useMemo } from "react";
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
  const [calendarRange, setCalendarRange] = useState({ start: null, end: null });

  const [selectedTask, setSelectedTask] = useState({
      id: '',
      groupId: '',
      day: '',
      date: "",
      start: '',
      end: '',
      topics: [],
      recurrent: true,
  });

  const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

  const [events, setEvents] = useState([]);

  const [clickedEvent, setClickedEvent] = useState(null);


  const handleSelect = (info) => {
 
    setCreated(false);
    const start = DateTime.fromISO(info.startStr);
    const end = DateTime.fromISO(info.endStr);
    
    setSelectedTask({
      topics: [],
      day: dias[new Date(start).getDay()],
      date: start.toFormat("yyyy-MM-dd"),
      start: start.toFormat("HH:mm"),
      end: end.toFormat("HH:mm"),
      recurrent: false,
    })
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleCancelTask = (taskName) => {
    setModalOpen(false);
  };

  const handleEventClick = (arg) => {
    
    let evento = {
      id        :   arg.event.id,
      groupId   :   arg.event?.groupId,
      title     :   arg.event.title,
      color     :   arg.event.color,
      start     :   arg.event.start,
      end       :   arg.event.end,
      extendedProps: {
          day         : arg.event.extendedProps.day,
          date        : arg.event.extendedProps.date,
          recurrent   : arg.event.extendedProps.recurrent,
          eventTopics : arg.event.extendedProps.eventTopics,
      }
    };

    setClickedEvent(evento);
    // console.log("arg.event.id: ", arg.event.id);
    // console.log("arg.event?.groupId: ", arg.event.groupId);
    // console.log("arg.event.title: ", arg.event.title);
    // console.log("arg.event.color: ", arg.event.color);
    // console.log("arg.event.extendedProps.day: ", arg.event.extendedProps.day);
    // console.log("arg.event.extendedProps.date: ", arg.event.extendedProps.date);
    // console.log("arg.event.start: ", arg.event.start);
    // console.log("arg.event.end: ", arg.event.end);
    // console.log("arg.event.extendedProps.recurrent: ", arg.event.extendedProps.recurrent);
    // console.log("arg.event.extendedProps.eventTopics: ", arg.event.extendedProps.eventTopics);
    console.log("evento: ", evento);

    setCreated(true);
    setModalOpen(true);
  };

  const handleSaveTask = (taskName) => {
    
    const startToCheck = combinarFechaYHora(taskName?.date, taskName.start);
    const endToCheck = combinarFechaYHora(taskName?.date, taskName.end);

    const haySolapamiento = events.some(ev => {
      const evStart = new Date(ev.start);
      const evEnd = new Date(ev.end);

      return (
        startToCheck.getTime() < evEnd.getTime() &&
        endToCheck.getTime() > evStart.getTime()
      );
    });

    if (!haySolapamiento) {
 
      if (taskName.recurrent) {
        createRecurrentEvent(taskName);
      }
      else {
        createEvent(taskName);
      }

      handleCloseModal();
      // return true;
    }
    else {
      alert("Error al crear evento, el rango horario ya contiene eventos.")
      // return false;
    }

  };

  const handleSaveEditTask = (event) => {

    
    setEvents((prevEvents) => {
      // if (event.extendedProps?.recurrent) {
    // Si es recurrente y el groupId coincide, actualizamos
    
    // return ev.groupId === event.groupId
    //   ? { ...event,
    //     id            : ev.id,
    //     start         : ev.start,
    //     end           : ev.end,
    //     extendedProps : {
      //       ...event.extendedProps,
      //       date        : ev.extendedProps.date,
      //     },
      //   }
      //   : ev;
      const firstMatch = prevEvents.find(ev => ev.groupId === event.groupId);
      const dayHasChanged = event.extendedProps.day !== firstMatch?.extendedProps.day;
      const dayOffset = dayHasChanged
      ? dias.indexOf(event.extendedProps.day) - dias.indexOf(firstMatch.extendedProps.day)
      : 0;

      return prevEvents.map((ev) => {
        if (event.extendedProps?.recurrent && ev.groupId === event.groupId) {
          // Ajustamos la fecha si el día cambió
          const originalDate = new Date(ev.extendedProps.date);
          const newDate = dayHasChanged
            ? new Date(originalDate.setDate(originalDate.getDate() + dayOffset))
            : originalDate;

          // Obtener la hora original de start y end
          const startTime = getTimeFromDate(ev.start); // e.g. "14:00:00"
          const endTime = getTimeFromDate(ev.end);

          // Generar nuevos start y end con la nueva fecha
          const newDateStr = newDate.toISOString().split('T')[0];
          const newStart = new Date(`${newDateStr}T${startTime}`);
          const newEnd = new Date(`${newDateStr}T${endTime}`);  


          return {
              ...event,
              id            : ev.id,
              start         : newStart,
              end           : newEnd,
              extendedProps : {
                ...event.extendedProps,
                date        : newDateStr,
              },
            };
            
        } else {
          // Si no es recurrente, actualizamos solo por id
          return ev.id === event.id ? event : ev;
        }
        
      });
    });

    handleCloseModal();
  }

  const handleDeleteTask = (event) => {

    const isEventRecurrent = event.extendedProps.recurrent;
  
    setEvents((prevEvents) => 
      prevEvents.filter((ev) => {
        // evento recurrente
        if (isEventRecurrent) {
          // Borrar todas las recurrencias con el mismo groupId
          const evGroupId = ev.groupId;
          return evGroupId !== event.groupId;
        }
        // evento no recurrente
        return ev.id !== event.id;
      })
    );

    handleCloseModal();
  }

  const handleCancelOneOccurrence = (event) => {

    event.extendedProps.recurrent = false;

    handleDeleteTask(event);

  };

  const createEvent = (taskName) => {
    
    const newEvent = {
      id      :     `${crypto.randomUUID()}`,
      title   :     '',
      color   :     'orange',          
      start   :     `${taskName.date}T${taskName.start}`,
      end     :     `${taskName.date}T${taskName.end}`,
 
      extendedProps : {
        day         : taskName.day,
        date        : taskName.date,
        recurrent   : taskName.recurrent,
        eventTopics : taskName.topics,
      },
    }

    setEvents([...events, 
      newEvent
    ]);
    
  }

  const createRecurrentEvent = (taskName) => {

    const current = new Date(calendarRange.start);
    const originalStart = taskName.start;
    const originalEnd = taskName.end;
    const groupIdGen = crypto.randomUUID();
    const newEvents = [];

    while (current <= calendarRange.end) {
      const currentDay = dias[current.getDay()];

      if (currentDay === taskName.day) {
        const dateStr = current.toISOString().split("T")[0];

        const newEvent = {
          id      :    `${crypto.randomUUID()}`,
          groupId :    `${groupIdGen}`,
          title   :    '',
          color   :    'green',          
          start   :    `${dateStr}T${originalStart}`,
          end     :    `${dateStr}T${originalEnd}`,
          extendedProps : {
                      date: dateStr,
                      day: currentDay,
                      recurrent: taskName.recurrent,
                      eventTopics: taskName.topics,
          },
        }

        newEvents.push(newEvent);
      };

      current.setDate(current.getDate() + 1);
    }

    setEvents(prevEvents => [...prevEvents, ...newEvents]);

  }
  
  function combinarFechaYHora(fecha, hora) {
    const base = `${fecha}T${hora.length === 5 ? hora + ':00' : hora}`; // asegura formato con segundos
    return new Date(base);
  }

  // Utilidad para extraer hora en formato "HH:MM:SS"
  function getTimeFromDate(date) {
    const d = new Date(date);
    return d.toTimeString().split(' ')[0];
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
        datesSet={ (info) => {
          setCalendarRange( {
            start : new Date(info.startStr),
            end : new Date(info.endStr),
            });
          }
        }
      />
      <>
        {isCreated ? (
          <ScheduleEdit
            open={modalOpen}
            clickedEvent={clickedEvent}
            onClose={handleCloseModal}
            taskData={selectedTask}
            onDeleteTask={handleDeleteTask}
            onCancelOneOccurrence={handleCancelOneOccurrence}
            onCancelTask={handleCancelTask}
            onSaveEditTask={handleSaveEditTask}
          />
        ) : (
          <ScheduleCreate
            open={modalOpen}
            onClose={handleCloseModal}
            taskData={selectedTask}
            onCancelTask={handleCancelTask}
            onSaveTask={handleSaveTask}
          />
        )}
      </>
    </div>
  );
}

export default Calendar;
