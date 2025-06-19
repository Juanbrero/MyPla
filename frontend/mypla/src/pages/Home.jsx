import '../App.css'
import { EventGrid } from '../components/homeBody/EventGrid'


function Home() {

const events = [
  {
    id: 1,
    title: "Taller de JavaScript Avanzado",
    date: "2025-06-21",
    hora: "10:00",
    precio: 1500,
    creator: "María López",
    participants: ["Juan Pérez", "Ana Torres"],
    category: "Programacion"
  },
  {
    id: 2,
    title: "Introducción al Universo",
    date: "2025-07-10",
    hora: "14:30",
    precio: 2000,
    creator: "Carlos Gómez",
    participants: [],
    category: "Astronomia"
  },
  {
    id: 3,
    title: "Álgebra para Principiantes",
    date: "2025-06-25",
    hora: "16:00",
    precio: 1200,
    creator: "Sofía Rodríguez",
    participants: ["Lucía González"],
    category: "Matematicas"
  },
  {
    id: 4,
    title: "Robótica Educativa en Secundaria",
    date: "2025-07-05",
    hora: "09:00",
    precio: 2500,
    creator: "Luis Fernández",
    participants: ["Julián Bravo", "Esteban Gil"],
    category: "Tecnologia"
  },
  {
    id: 5,
    title: "Taller de React + FastAPI",
    date: "2025-06-29",
    hora: "18:00",
    precio: 3000,
    creator: "Valentina Castro",
    participants: [],
    category: "Programacion"
  },
  {
    id: 6,
    title: "Noches de Astronomía: Observación del Cielo",
    date: "2025-07-12",
    hora: "20:00",
    precio: 1800,
    creator: "Gustavo Luna",
    participants: ["Astrónomos invitados"],
    category: "Astronomia"
  },
  {
    id: 7,
    title: "Cálculo I Intensivo",
    date: "2025-07-03",
    hora: "11:00",
    precio: 1600,
    creator: "Fernando Martínez",
    participants: [],
    category: "Matematicas"
  },
  {
    id: 8,
    title: "Python para Análisis de Datos",
    date: "2025-07-08",
    hora: "17:00",
    precio: 2800,
    creator: "Camila Ortega",
    participants: ["Laura Vega"],
    category: "Programacion"
  },
  {
    id: 9,
    title: "Noche de Ciencias: Taller con Experimentos",
    date: "2025-06-30",
    hora: "19:00",
    precio: 1900,
    creator: "Mariano Torres",
    participants: ["Equipo Científico Escolar"],
    category: "Ciencias"
  },
  {
    id: 10,
    title: "Introducción a Machine Learning",
    date: "2025-07-15",
    hora: "13:00",
    precio: 3200,
    creator: "Natalia Domínguez",
    participants: [],
    category: "Programacion"
  }
];


  return (
    <>
      <div className='homeBody-container'>

        <h1 className='welcome-title'>Bienvenido a <span>MiPla!</span></h1>
        
        <EventGrid events={events} />
      </div>

    </>
  )
}

export default Home
