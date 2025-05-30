import React, { useState, useEffect } from "react";
import ScheduleEdit from '../components/ScheduleEdit';
import ScheduleCreate from '../components/ScheduleCreate';
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { DateTime } from "luxon";
import { useAuth0 } from "@auth0/auth0-react";
import { deleteSpecific, postSpecific }  from "../services/specific/specific.service";
import { getAvailableProfessional } from "../services/available/available-professional.service";
import { dateObjToLocalTime } from "../utils/dateFormater";
import './calendar.css';


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
      // recurrent: true,
      category: "",
  });
  const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const [events, setEvents] = useState([]);

  const [dbEvents, setDbEvents] = useState([]);
  
  const [specifics, setSpecifics] = useState([]);
  const [recurrents, setRecurrents] = useState([]);
  const [exceptions, setExceptions] = useState([]);

  const [clickedEvent, setClickedEvent] = useState(null);

  
  useEffect(() => {
    const fetchProfessional = async () => {

      const { data, error } = await getAvailableProfessional();

      if (error) {
        console.log(error);
      } else {

        const specific = data.specific;
        setSpecifics(specific);
        
        const recurrent = data.recurrent;
        setRecurrents(recurrent);

        const exception = data.exception;
        setExceptions(exception);

        // const clase = data.class_;
        // setDbEvents([...specific, ...recurrent, ...exception, ...class_]);

        setDbEvents([...specific, ...recurrent, ...exception]);

      }
    };

    fetchProfessional();
  }, [refreshTrigger]);


  const handleSelect = (info) => {
 
    console.log("dbEvents: ", dbEvents);

    setCreated(false);
    const start = DateTime.fromISO(info.startStr);
    const end = DateTime.fromISO(info.endStr);
    
    setSelectedTask({
      topics: [],
      day: dias[new Date(start).getDay()],
      date: start.toFormat("yyyy-MM-dd"),
      start: start.toFormat("HH:mm"),
      end: end.toFormat("HH:mm"),
      category: 'specific',
      // recurrent: false,
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
    
    const startFormateado = dateObjToLocalTime(arg.event.start);

    let protoEvent = {
      start     :   startFormateado,
      extendedProps: {
          day         : arg.event.extendedProps.day,
          date        : arg.event.extendedProps.date,
          category    : arg.event.extendedProps.category,
      }
    };

    let evFound = searchEvent(protoEvent);

    setClickedEvent(evFound);
    setCreated(true);
    setModalOpen(true);
  };

  const handleSaveTask = async (taskName) => {
    
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
 
      if (taskName.category === "recurrent") {
        await createRecurrentEvent(taskName);
      }
      else {
        await createEvent(taskName);
      }

      handleCloseModal();
      // return true;
      setRefreshTrigger(prev => prev + 1);
    }
    else {
      alert("Error al crear evento, el rango horario ya contiene eventos.")
      // return false;
    }

  };

  const handleSaveEditTask = async (event) => {

    const foundEv = searchEvent(event);

    if (foundEv) {
      switch (foundEv.extendedProps.category) {
        case "specific":
          console.log("update foundEv: ", foundEv);
          await deleteSpecific("token", foundEv);
          break;
        case "recurrent":
          break;
        case "exception":
          break;
        case "class_":
          break;
      }
    }

    setEvents((prevEvents) => {

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
    // setEvents((prevEvents) => {

    //   const firstMatch = prevEvents.find(ev => ev.groupId === event.groupId);
    //   const dayHasChanged = event.extendedProps.day !== firstMatch?.extendedProps.day;
    //   const dayOffset = dayHasChanged
    //   ? dias.indexOf(event.extendedProps.day) - dias.indexOf(firstMatch.extendedProps.day)
    //   : 0;

    //   return prevEvents.map((ev) => {
    //     if (event.extendedProps?.recurrent && ev.groupId === event.groupId) {
    //       // Ajustamos la fecha si el día cambió
    //       const originalDate = new Date(ev.extendedProps.date);
    //       const newDate = dayHasChanged
    //         ? new Date(originalDate.setDate(originalDate.getDate() + dayOffset))
    //         : originalDate;

    //       // Obtener la hora original de start y end
    //       const startTime = getTimeFromDate(ev.start); // e.g. "14:00:00"
    //       const endTime = getTimeFromDate(ev.end);

    //       // Generar nuevos start y end con la nueva fecha
    //       const newDateStr = newDate.toISOString().split('T')[0];
    //       const newStart = new Date(`${newDateStr}T${startTime}`);
    //       const newEnd = new Date(`${newDateStr}T${endTime}`);  


    //       return {
    //           ...event,
    //           id            : ev.id,
    //           start         : newStart,
    //           end           : newEnd,
    //           extendedProps : {
    //             ...event.extendedProps,
    //             date        : newDateStr,
    //           },
    //         };
            
    //     } else {
    //       // Si no es recurrente, actualizamos solo por id
    //       return ev.id === event.id ? event : ev;
    //     }
        
    //   });
    // });

    handleCloseModal();
  }

  const handleDeleteTask = async (event) => {

    const foundEv = searchEvent(event);

    if (foundEv) {
      switch (foundEv.extendedProps.category) {
        case "specific":
          console.log("borrando foundEv: ", foundEv);
          await deleteSpecific("token", foundEv);
          break;
        case "recurrent":
          break;
        case "exception":
          break;
        case "class_":
          break;
      }
    }

    handleCloseModal();
    setRefreshTrigger(prev => prev + 1);

  }

  const handleCancelOneOccurrence = (event) => {

    event.extendedProps.recurrent = false;

    handleDeleteTask(event);

  };

  const createEvent = async (taskName) => {
    
    const newEvent = {
      id      :     `${crypto.randomUUID()}`,
      title   :     '',
      color   :     'orange',          
      start   :     `${taskName.date}T${taskName.start}`,
      end     :     `${taskName.date}T${taskName.end}`,
 
      extendedProps : {
        day         : taskName.day,
        date        : taskName.date,
        // recurrent   : taskName.recurrent,
        category    : taskName.category,
        eventTopics : taskName.topics,
      },
    }

    // setEvents([...events, 
    //   newEvent
    // ]);
    
    await postSpecific("token", newEvent);
  }

  const createRecurrentEvent =  async (taskName) => {

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
  
  const searchEvent = (event) => {

    const evCategory = event.extendedProps.category;
    let foundEv = {};

    switch (evCategory) {
      case "specific":
        foundEv = specifics.find(ev => ((ev.start === event.start) &&
                                  (ev.extendedProps.date === event.extendedProps.date)));
        break;
      case "recurrent":
        break;
      case "exception":
        break;
      case "class_":
        break;
    }

    return foundEv;

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
        initialView="timeGridWeek"
        headerToolbar={{
          start: "today prev,next",
          center: "title",
          end: "dayGridMonth,timeGridWeek",
        }}
        slotDuration="01:00:00"
        allDaySlot={false}
        selectable={true}
        select={handleSelect}
        eventClick={handleEventClick}
        events={Object.values(dbEvents).flat()}
        height={"90vh"}
        expandRows={true}
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
