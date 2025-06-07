import { useState } from 'react'
import '../App.css'
import { LoginButton } from '../components/auth0Buttons/LoginButton'
import { SignupButton } from '../components/auth0Buttons/SignUpButton'
import ReservationModal from '../components/reservation/ReservationModal'

function Home() {
  const [openModal, setOpenModal] = useState(false);

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

    </>
  )
}

export default Home
