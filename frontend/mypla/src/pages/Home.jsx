import { useState, useEffect } from 'react';
import '../App.css'
import { EventGrid } from '../components/homeBody/EventGrid'
import { getEvents } from '../services/events/events.service'
import { useAuth0 } from "@auth0/auth0-react";
import ReservationModal from '../components/reservation/ReservationModal';
import { Paginator } from '../components/paginator/Paginator';


function Home(token) {

  const [events, setEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(true);
  const EVENTS_PER_PAGE = 6;

  const { isAuthenticated } = useAuth0();
  const { loginWithRedirect } = useAuth0();
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null); 
  const [EventProf_id, setEventProfId] = useState(""); 

  
  useEffect(() => {
      const cargarEventos = async () => {
          try {

              const data = await getEvents(currentPage, EVENTS_PER_PAGE);
              console.log("cant events: ", data.length);
              console.log("page: ", currentPage, "amount: ", EVENTS_PER_PAGE);
              setEvents(data.events);
              setHasNextPage(currentPage < data.total_pages);
          } catch (error) {
              console.error("Error al obtener eventos:", error);
          }
      };
  
      cargarEventos();

  }, [currentPage]);

  // --- cierro el modal ------------------------------------------------------------------------
  const handleCloseModal = () => {
      setModalOpen(false);
      setModalData(null);
  };


  const selectEvent = async (event) => {

    if (isAuthenticated) {

      const [date, hour] = event.day_hour.split("T");
      const [hours, minutes] = hour.split(":");
      const formattedHour = `${hours}:${minutes}`;

      const selectedEvent = {
        ...event,
        date: date,
        hour: formattedHour,
      }

      setModalData(selectedEvent);
      setEventProfId(event.prof_id);
      setModalOpen(true);

    }
    else {
      await loginWithRedirect({
        appState: {
          returnTo: "/",
        },
        authorizationParams: {
          prompt: "login",
        },
      });
    }

  }
  

  return (
    <>
      <div className='homeBody-container'>

        <h1 className='welcome-title'>Bienvenido a <span>MiPla!</span></h1>
        
        <EventGrid events={events} onSelectEvent={selectEvent}/>
      </div>

      <Paginator
        currentPage={currentPage}
        hasNextPage={hasNextPage}
        onPageChange={(page) => setCurrentPage(page)}
      />


      <ReservationModal
          open={modalOpen}
          onClose={handleCloseModal}
          event={modalData}
          token={token}
          prof_id={EventProf_id}
      />

    </>
  )
}

export default Home
