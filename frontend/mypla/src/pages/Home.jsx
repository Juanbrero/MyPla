import { useState } from 'react'
import '../App.css'
import { LoginButton } from '../components/auth0Buttons/LoginButton'
import { SignupButton } from '../components/auth0Buttons/SignUpButton'
import ReservationModal from '../components/reservation/ReservationModal'

function Home() {
  const [count, setCount] = useState(0);
  const [openModal, setOpenModal] = useState(false);
  
  const taskData= {
    start: `11:00:00.000Z`,
    end: `14:00:00.000Z`,
    topics: ["ESTRATEGIA, PROGRAMACION, VENTAS"],
    avaliableTopics: ["ESTRATEGIA, PROGRAMACION"],
    day: "2025-05-31", //si es recurrente envio el dia en que se clickea para la generacion de excepciones
    week_day: 6,
    recurrent: false,
    // selectedHour: toISO8601(hora),
    // tipo: evento.type
  }

  const closeModal = () => {
    setOpenModal(false);
  }

  const testReserva = () => {
    return setOpenModal(true);
  }

  return (
    <>
      
      <h1>Bienvenido a <span style={{color: '#1cb6ae'}}>MiPla!</span></h1>
      
      <div className='loginButtons'>
        <LoginButton />
        <SignupButton />
      </div>
      <div>
        <button onClick={testReserva} style={{marginTop: '100px'}}>Test componente reserva de horario</button>
        <ReservationModal open={openModal} onClose={closeModal} taskData={taskData}></ReservationModal>
      </div>

    </>
  )
}

export default Home
