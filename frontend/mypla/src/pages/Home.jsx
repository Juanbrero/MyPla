import { useState, useEffect } from 'react';
import '../App.css'
import { EventGrid } from '../components/homeBody/EventGrid'
import { getEvents } from '../services/events/events.service'
import { useAuth0 } from "@auth0/auth0-react";
import ReservationModal from '../components/reservation/ReservationModal';


function Home(token) {

const events = [
  {
    prof_id: 0,
    title: "Taller de JavaScript Avanzado",
    date: "2025-06-21",
    hour: "10:00",
    precio: 1500,
    creator: "María López",
    participants: ["Juan Pérez", "Ana Torres"],
    topic: "Programacion"
  },
  {
    prof_id: 1,
    title: "Introducción al Universo",
    date: "2025-07-10",
    hour: "14:30",
    precio: 2000,
    creator: "Carlos Gómez",
    participants: [],
    topic: "Astronomia"
  },
  {
    prof_id: 2,
    title: "Álgebra para Principiantes",
    date: "2025-06-25",
    hour: "16:00",
    precio: 1200,
    creator: "Sofía Rodríguez",
    participants: ["Lucía González"],
    topic: "Matematicas"
  },
  {
    prof_id: 3,
    title: "Robótica Educativa en Secundaria",
    date: "2025-07-05",
    hour: "09:00",
    precio: 2500,
    creator: "Luis Fernández",
    participants: ["Julián Bravo", "Esteban Gil"],
    topic: "Tecnologia"
  },
  {
    prof_id: 4,
    title: "Taller de React + FastAPI",
    date: "2025-06-29",
    hour: "18:00",
    precio: 3000,
    creator: "Valentina Castro",
    participants: [],
    topic: "Baile"
  },
  {
    prof_id: 5,
    title: "Noches de Astronomía: Observación del Cielo",
    date: "2025-07-12",
    hour: "20:00",
    precio: 1800,
    creator: "Gustavo Luna",
    participants: ["Astrónomos invitados"],
    topic: "Literatura"
  },
  {
    prof_id: 6,
    title: "Cálculo I Intensivo",
    date: "2025-07-03",
    hour: "11:00",
    precio: 1600,
    creator: "Fernando Martínez",
    participants: [],
    topic: "Geografia"
  },
  {
    prof_id: 7,
    title: "Python para Análisis de Datos",
    date: "2025-07-08",
    hour: "17:00",
    precio: 2800,
    creator: "Camila Ortega",
    participants: ["Laura Vega"],
    topic: "Guitarra"
  },
  {
    prof_id: 8,
    title: "Noche de Ciencias: Taller con Experimentos",
    date: "2025-06-30",
    hour: "19:00",
    precio: 1900,
    creator: "Mariano Torres",
    participants: ["Equipo Científico Escolar"],
    topic: "Ciencias"
  },
  {
    prof_id: 9,
    title: "Introducción a Machine Learning",
    date: "2025-07-15",
    hour: "13:00",
    precio: 3200,
    creator: "Natalia Domínguez",
    participants: [],
    topic: "Python"
  },
  {
    prof_id: 10,
    title: "Introducción a Machine Learning",
    date: "2025-07-15",
    hour: "13:00",
    precio: 3200,
    creator: "Natalia Domínguez",
    participants: [],
    topic: "Periodismo"
  }
];

  // const [events, setEvents] = useState([]);

  const { isAuthenticated } = useAuth0();
  const { loginWithRedirect } = useAuth0();
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null); 
  const [prof_id, setProfId] = useState(); 

  
  useEffect(() => {
      const cargarEventos = async () => {
          try {
              // const data = await getEvents();
              // setEvents(prevEvents => [...prevEvents, ...data]);
          } catch (error) {
              console.error("Error al obtener eventos:", error);
          }
      };
  
      cargarEventos();

  }, []);

  // --- cierro el modal ------------------------------------------------------------------------
  const handleCloseModal = () => {
      setModalOpen(false);
      setModalData(null);
  };


  const selectEvent = async (event) => {

    if (isAuthenticated) {
      setModalData(event);
      setProfId(event.prof_id);
      setModalOpen(true);
      console.log(event);
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

      <ReservationModal
          open={modalOpen}
          onClose={handleCloseModal}
          event={modalData}
          token={token}
          prof_id={prof_id}
      />

    </>
  )
}

export default Home
