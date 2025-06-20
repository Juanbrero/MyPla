import { useState, useEffect } from 'react';
import '../App.css'
import { EventGrid } from '../components/homeBody/EventGrid'
import { getEvents } from '../services/events/events.service'
import { useAuth0 } from "@auth0/auth0-react";


function Home(token) {

const events = [
  {
    title: "Taller de JavaScript Avanzado",
    date: "2025-06-21",
    hora: "10:00",
    precio: 1500,
    creator: "María López",
    participants: ["Juan Pérez", "Ana Torres"],
    category: "Programacion"
  },
  {
    title: "Introducción al Universo",
    date: "2025-07-10",
    hora: "14:30",
    precio: 2000,
    creator: "Carlos Gómez",
    participants: [],
    category: "Astronomia"
  },
  {
    title: "Álgebra para Principiantes",
    date: "2025-06-25",
    hora: "16:00",
    precio: 1200,
    creator: "Sofía Rodríguez",
    participants: ["Lucía González"],
    category: "Matematicas"
  },
  {

    title: "Robótica Educativa en Secundaria",
    date: "2025-07-05",
    hora: "09:00",
    precio: 2500,
    creator: "Luis Fernández",
    participants: ["Julián Bravo", "Esteban Gil"],
    category: "Tecnologia"
  },
  {

    title: "Taller de React + FastAPI",
    date: "2025-06-29",
    hora: "18:00",
    precio: 3000,
    creator: "Valentina Castro",
    participants: [],
    category: "Baile"
  },
  {

    title: "Noches de Astronomía: Observación del Cielo",
    date: "2025-07-12",
    hora: "20:00",
    precio: 1800,
    creator: "Gustavo Luna",
    participants: ["Astrónomos invitados"],
    category: "Literatura"
  },
  {

    title: "Cálculo I Intensivo",
    date: "2025-07-03",
    hora: "11:00",
    precio: 1600,
    creator: "Fernando Martínez",
    participants: [],
    category: "Geografia"
  },
  {
 
    title: "Python para Análisis de Datos",
    date: "2025-07-08",
    hora: "17:00",
    precio: 2800,
    creator: "Camila Ortega",
    participants: ["Laura Vega"],
    category: "Guitarra"
  },
  {

    title: "Noche de Ciencias: Taller con Experimentos",
    date: "2025-06-30",
    hora: "19:00",
    precio: 1900,
    creator: "Mariano Torres",
    participants: ["Equipo Científico Escolar"],
    category: "Ciencias"
  },
  {

    title: "Introducción a Machine Learning",
    date: "2025-07-15",
    hora: "13:00",
    precio: 3200,
    creator: "Natalia Domínguez",
    participants: [],
    category: "Python"
  },
  {

    title: "Introducción a Machine Learning",
    date: "2025-07-15",
    hora: "13:00",
    precio: 3200,
    creator: "Natalia Domínguez",
    participants: [],
    category: "Periodismo"
  }
];

  // const [events, setEvents] = useState([]);

  const { isAuthenticated } = useAuth0();
  const { loginWithRedirect } = useAuth0();
  
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


  const selectEvent = async (event) => {

    if (isAuthenticated) {
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

    </>
  )
}

export default Home
